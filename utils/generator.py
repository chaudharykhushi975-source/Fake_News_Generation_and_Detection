import random
import nltk
from textblob import TextBlob
import re

class FakeNewsGenerator:
    def __init__(self):
        # Common fake news patterns and templates
        self.templates = [
            "BREAKING: {subject} {action} {detail}",
            "EXCLUSIVE: {subject} {action} {detail}",
            "SHOCKING: {subject} {action} {detail}",
            "URGENT: {subject} {action} {detail}",
            "ALERT: {subject} {action} {detail}"
        ]
        
        self.subjects = [
            "the government", "scientists", "experts", "officials",
            "the president", "WHO", "CDC", "NASA", "the UN"
        ]
        
        self.actions = [
            "confirmed", "announced", "revealed", "discovered",
            "warned about", "investigated", "declared", "proved"
        ]
        
        self.details = [
            "a major cover-up", "a new threat", "an alarming discovery",
            "a conspiracy", "the truth about", "evidence of",
            "a secret operation", "the real story behind"
        ]
        
        self.conspiracy_phrases = [
            "The truth is being hidden from you.",
            "This is what they don't want you to know.",
            "The mainstream media won't tell you this.",
            "Only we have access to this information.",
            "This changes everything we thought we knew."
        ]
        
    def generate_fake_news(self, topic=None):
        """Generate a fake news article"""
        if topic:
            subject = topic
        else:
            subject = random.choice(self.subjects)
        
        action = random.choice(self.actions)
        detail = random.choice(self.details)
        
        # Generate headline
        template = random.choice(self.templates)
        headline = template.format(
            subject=subject.title(),
            action=action,
            detail=detail
        )
        
        # Generate body
        body = self._generate_body(subject, action, detail)
        
        # Add a sensational claim
        claim = random.choice(self.conspiracy_phrases)
        
        return {
            'headline': headline,
            'body': body,
            'claim': claim,
            'full_text': f"{headline}\n\n{body}\n\n{claim}"
        }
    
    def _generate_body(self, subject, action, detail):
        """Generate the body of the news article"""
        bodies = [
            f"According to anonymous sources, {subject} {action} {detail}. "
            f"This discovery has sent shockwaves through the scientific community.",
            
            f"In a stunning development, {subject} {action} {detail}. "
            f"Experts are calling this the most significant finding of the decade.",
            
            f"New evidence suggests that {subject} {action} {detail}. "
            f"This revelation contradicts everything we thought we knew.",
            
            f"An insider has leaked information that {subject} {action} {detail}. "
            f"The implications of this are far-reaching and potentially catastrophic.",
        ]
        
        return random.choice(bodies)
    
    def modify_real_news(self, real_text):
        """Modify real news to create fake news"""
        # Simple modifications
        replacements = {
            'confirmed': 'allegedly confirmed',
            'reported': 'secretly reported',
            'study': 'flawed study',
            'experts': 'so-called experts',
            'evidence': 'questionable evidence'
        }
        
        for word, replacement in replacements.items():
            real_text = real_text.replace(word, replacement)
        
        # Add sensational phrases
        sensational_phrases = [
            "This is a cover-up! ",
            "The public deserves to know the truth! ",
            "This is just the tip of the iceberg. "
        ]
        
        real_text = random.choice(sensational_phrases) + real_text
        
        return real_text