import re
import json
from typing import List

from .text import TextBlock
from .code import CodeBlock
from .divider import DividerBlock
from .heading import HeadingBlock
from .link import LinkBlock
from .button import ButtonBlock


class BlockParser:
    """
    Deterministic, non-LLM parser for ChatBubble blocks.
    """

    CODE_PATTERN = re.compile(
        r"```(\w+)?\n(.*?)```",
        re.S
    )

    HEADING_PATTERN = re.compile(
        r"^(#{1,4})\s+(.*)$",
        re.M
    )

    LINK_PATTERN = re.compile(
        r"\[([^\]]+)\]\(([^)]+)\)"
    )

    BUTTON_PATTERN = re.compile(
        r"\[\[button:(.*?)\|(.*?)\]\]"
    )

    DIVIDER_PATTERN = re.compile(
        r"^\s*---\s*$",
        re.M
    )

    def parse(self, text: str) -> List:
        blocks = []
        cursor = 0

        # Step 1: extract code blocks first
        for match in self.CODE_PATTERN.finditer(text):
            if match.start() > cursor:
                blocks.extend(self._parse_inline(text[cursor:match.start()]))
            
            lang = match.group(1) or "text"
            code = match.group(2).strip()
            blocks.append(CodeBlock(code, lang))

            cursor = match.end()
        
        if cursor < len(text):
            blocks.extend(self._parse_inline(text[cursor:]))
        
        return blocks
    
    def _parse_inline(self, text: str) -> List:
        blocks = []
        lines = text.splitlines()

        for line in lines:
            # Divider
            if self.DIVIDER_PATTERN.match(line):
                blocks.append(DividerBlock())
                continue

            # Heading
            h = self.HEADING_PATTERN.match(line)
            if h:
                level = len(h.group(1))
                blocks.append(HeadingBlock(h.group(2), level))
                continue

            # Button
            btn = self.BUTTON_PATTERN.search(line)
            if btn:
                label = btn.group(1).strip()
                try:
                    payload = json.loads(btn.group(2))
                except Exception:
                    payload = {}
                blocks.append(ButtonBlock(label, payload))
                continue

            # Links (inline replacement)
            last = 0
            for lm in self.LINK_PATTERN.finditer(line):
                if lm.start() > last:
                    blocks.append(TextBlock(line[last:lm.start()]))
                
                blocks.append(LinkBlock(lm.group(1), lm.group(2)))
                last = lm.end()
            
            if last < len(line):
                blocks.append(TextBlock(line[last:]))
        
        return blocks