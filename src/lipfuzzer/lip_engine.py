"""Fuzzing Engine for Voice Assistant security testing."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lipfuzzer.io.rule_io import rulePack, RuleDict
from lipfuzzer.io.utterance_io import UtterancePack
from lipfuzzer.nlp_engine import NLPEngine

sys.path.append("./modules/")
from modules import *

# Import TTS module for speech synthesis
try:
    from tts.deepgram_tts import DeepgramTTS

    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("Warning: TTS module not available. Install deepgram-sdk for speech synthesis.")

# Import LLM module for command generation
try:
    from llm import create_llm_client
    from llm.prompts import PromptManager

    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("Warning: LLM module not available. Install LLM dependencies for command generation.")


class lipEngine:
    """Main fuzzing engine for voice assistant security testing."""

    def __init__(self, outPath: str = "out.txt") -> None:
        """Initialize the fuzzing engine.

        Args:
            outPath: Output file path for fuzzing results
        """
        self.readRuleSet: dict[str, RuleDict] = {}
        self.outPath = outPath
        self.supportedModule = [0, 1, 2, 3, 4, 5, 6, 7]
        self.tts_client: DeepgramTTS | None = None
        self.llm_client: Any | None = None
        self.prompt_manager: PromptManager | None = None

        # Initialize TTS client if available
        if TTS_AVAILABLE:
            try:
                self.tts_client = DeepgramTTS()
                print("[lipEngine] TTS client initialized")
            except Exception as e:
                print(f"[lipEngine] Failed to initialize TTS: {e}")

        # Initialize LLM client if available
        if LLM_AVAILABLE:
            try:
                self.llm_client = create_llm_client()
                self.prompt_manager = PromptManager()
                print("[lipEngine] LLM client initialized")
            except Exception as e:
                print(f"[lipEngine] Failed to initialize LLM: {e}")

    def loadRule(self, path: str) -> None:
        """Load fuzzing rules from file.

        Args:
            path: Path to rules file
        """
        print("\n[lipEngine] Loading rules")

        r = rulePack()
        r.readRule(path)
        self.readRuleSet = r.getReadRuleSet()

        for rule in self.readRuleSet.values():
            if rule["module"] not in self.supportedModule:
                print(f"Module {rule['module']} not supported")

    def loadData(self, path: str) -> None:
        """Load test data from file.

        Args:
            path: Path to data file
        """
        print("[lipEngine] Loading data\n")

        self.uu = UtterancePack()
        self.uu.filePath = path
        self.uu.reading()
        self.nlp = NLPEngine()

        for key, value in self.uu.readUtteranceSet.items():
            print(f"===============>> {value['ut']}")
            value["to"] = self.nlp.tokenize(value["ut"])
            value["de"] = self.nlp.depParse(value["ut"])
            value["ph"] = {}
            value["le"] = {}

            for ind, token in enumerate(value["to"]):
                value["le"][ind] = self.nlp.lemmatization(token)
                value["ph"][ind] = self.nlp.phonimizer(token)

            print(str(value))

    def fuzz(
        self,
        rules: list[int] | None = None,
        INHERITCHANGE: bool = False,
        OUTPUTSTEP: bool = False,
    ) -> None:
		print("\n[lipEngine] Fuzzing...\n")

		if len(rules) == 0:
			rules = sorted(self.readRuleSet.keys())

		for key, value in self.uu.readUtteranceSet.items():
			data = value.copy()
			applied_rule = []

			print("Input: ")
			print(str(data))

			for rule_id in rules:
				if not INHERITCHANGE:
					data = value.copy()
					applied_rule = ["r" + str(rule_id) + "m" + str(self.readRuleSet[rule_id]['module'])]
				else:
					applied_rule.append("r" + str(rule_id) + "m" + str(self.readRuleSet[rule_id]['module']))
					
				#~ print(".....+++++")
				#~ print self.readRuleSet[rule_id]['module']
				#~ print self.readRuleSet[rule_id]
				out = self.execModule(self.readRuleSet[rule_id]['module'], data, self.readRuleSet[rule_id])

				if OUTPUTSTEP:
					print("\nRules applied: " + str(applied_rule))
					
					if out is not None and str(out).strip() is not None:
						print("[Result]: " + str(out))
					#~ else:
						#~ print "Result: " + str(data) + "\n"

			if not OUTPUTSTEP:
				print("Final Output: ")
				print(str(data))

			print("==============\n")
				
	def execModule(self, mod_id, data, rule):
		out = ""
		p = inflect.engine()
		mod_name = "module_" + str(p.number_to_words(mod_id))
		print(mod_name)
		exec("out = " + mod_name + "." + mod_name + "(self, data, rule)")
		return out
	
	def synthesize_speech(self, text, output_path, voice=None):
		"""
		Synthesize speech from text using TTS client.
		
		Args:
			text: Text to synthesize
			output_path: Path to save audio file
			voice: Optional voice model override
			
		Returns:
			True if successful, False otherwise
		"""
		if not self.tts_client:
			print("[lipEngine] TTS client not available")
			return False
		
		try:
			return self.tts_client.synthesize(text, output_path, voice)
		except Exception as e:
			print(f"[lipEngine] Speech synthesis failed: {e}")
			return False
	
	def verify_utterance(self, utterance_text, output_audio_path=None):
		"""
		Verify an utterance by synthesizing it to speech.
		
		Args:
			utterance_text: The utterance text to verify
			output_audio_path: Optional path to save audio (auto-generated if None)
			
		Returns:
			Path to generated audio file if successful, None otherwise
		"""
		if output_audio_path is None:
			# Auto-generate output path
			import os
			import time
			audio_dir = "verification_audio"
			os.makedirs(audio_dir, exist_ok=True)
			timestamp = int(time.time() * 1000)
			output_audio_path = os.path.join(audio_dir, f"verify_{timestamp}.mp3")
		
		if self.synthesize_speech(utterance_text, output_audio_path):
			print(f"[lipEngine] Verification audio saved: {output_audio_path}")
			return output_audio_path
		else:
			return None
	
	# ===== LLM Command Generation Methods =====
	
	def generate_seed_commands(self, 
	                          assistant="Alexa",
	                          domain="smart_home",
	                          count=10,
	                          template="seed_generation"):
		"""
		Generate initial seed voice commands using LLM.
		
		Args:
			assistant: Voice assistant name (e.g., 'Alexa', 'Hey Google', 'Siri')
			domain: Application domain (e.g., 'smart_home', 'banking', 'e-commerce')
			count: Number of commands to generate
			template: Prompt template name to use
			
		Returns:
			List of generated command strings
		"""
		if not self.llm_client:
			print("[lipEngine] LLM client not available")
			return []
		
		try:
			context = {
				'assistant': assistant,
				'domain': domain,
				'count': count
			}
			
			commands = self.llm_client.generate_commands(context, template, count)
			print(f"[lipEngine] Generated {len(commands)} seed commands")
			return commands
			
		except Exception as e:
			print(f"[lipEngine] Failed to generate seed commands: {e}")
			return []
	
	def generate_mutations(self,
	                      original_command,
	                      mutation_type="phonetic",
	                      count=5,
	                      template="mutation_generation"):
		"""
		Generate LLM-based mutations of an existing command.
		
		Args:
			original_command: The original voice command to mutate
			mutation_type: Type of mutation ('phonetic', 'semantic', 'syntactic')
			count: Number of mutations to generate
			template: Prompt template name to use
			
		Returns:
			List of mutated command strings
		"""
		if not self.llm_client:
			print("[lipEngine] LLM client not available")
			return []
		
		try:
			context = {
				'original_command': original_command,
				'mutation_type': mutation_type,
				'count': count
			}
			
			mutations = self.llm_client.generate_commands(context, template, count)
			print(f"[lipEngine] Generated {len(mutations)} mutations")
			return mutations
			
		except Exception as e:
			print(f"[lipEngine] Failed to generate mutations: {e}")
			return []
	
	def generate_adversarial_commands(self,
	                                 assistant="Alexa",
	                                 target_domain="banking",
	                                 count=10,
	                                 template="adversarial_generation"):
		"""
		Generate adversarial commands for security testing.
		
		Args:
			assistant: Target voice assistant
			target_domain: Application domain to target
			count: Number of adversarial commands to generate
			template: Prompt template name to use
			
		Returns:
			List of adversarial command strings
		"""
		if not self.llm_client:
			print("[lipEngine] LLM client not available")
			return []
		
		try:
			context = {
				'assistant': assistant,
				'domain': target_domain,
				'count': count
			}
			
			commands = self.llm_client.generate_commands(context, template, count)
			print(f"[lipEngine] Generated {len(commands)} adversarial commands")
			return commands
			
		except Exception as e:
			print(f"[lipEngine] Failed to generate adversarial commands: {e}")
			return []
	
	def generate_and_synthesize(self,
	                           prompt_template,
	                           context,
	                           output_dir="generated_audio",
	                           voice=None,
	                           prefix="cmd"):
		"""
		Generate commands with LLM and synthesize them to audio files.
		
		Args:
			prompt_template: Template name or prompt string
			context: Dictionary with template variables (must include 'count')
			output_dir: Directory to save audio files
			voice: Optional voice model override
			prefix: Prefix for audio filenames
			
		Returns:
			List of tuples: [(command_text, audio_path), ...]
		"""
		if not self.llm_client:
			print("[lipEngine] LLM client not available")
			return []
		
		if not self.tts_client:
			print("[lipEngine] TTS client not available")
			return []
		
		try:
			import os
			
			# Ensure output directory exists
			os.makedirs(output_dir, exist_ok=True)
			
			# Generate commands
			count = context.get('count', 10)
			commands = self.llm_client.generate_commands(context, prompt_template, count)
			
			if not commands:
				print("[lipEngine] No commands generated")
				return []
			
			print(f"[lipEngine] Synthesizing {len(commands)} commands to audio...")
			
			# Synthesize each command
			results = []
			for idx, command in enumerate(commands):
				audio_path = os.path.join(output_dir, f"{prefix}_{idx}.mp3")
				
				if self.tts_client.synthesize(command, audio_path, voice):
					results.append((command, audio_path))
					print(f"  [{idx+1}/{len(commands)}] {command} -> {audio_path}")
				else:
					print(f"  [{idx+1}/{len(commands)}] Failed: {command}")
			
			print(f"[lipEngine] Successfully synthesized {len(results)}/{len(commands)} commands")
			return results
			
		except Exception as e:
			print(f"[lipEngine] Failed to generate and synthesize: {e}")
			return []
	
	def generate_with_custom_prompt(self, prompt, count=10):
		"""
		Generate commands using a custom prompt string.
		
		Args:
			prompt: Custom prompt text
			count: Number of commands to generate
			
		Returns:
			List of generated command strings
		"""
		if not self.llm_client:
			print("[lipEngine] LLM client not available")
			return []
		
		try:
			# Add count instruction to prompt if not present
			if '{count}' in prompt:
				prompt = prompt.format(count=count)
			elif str(count) not in prompt:
				prompt = f"{prompt}\n\nGenerate {count} commands."
			
			response = self.llm_client.generate(prompt)
			commands = self.llm_client.parse_commands_from_response(response)
			
			print(f"[lipEngine] Generated {len(commands)} commands from custom prompt")
			return commands[:count]
			
		except Exception as e:
			print(f"[lipEngine] Failed to generate with custom prompt: {e}")
			return []

# ~ l = lipEngine()
# ~ l.loadRule("data/ruleFile.txt")
# ~ l.loadData("data/datashort.txt")
# ~l.fuzz(OUTPUTSTEP=True)
