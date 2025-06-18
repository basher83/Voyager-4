# Claude Code Prompt Engineering Best Practices

This guide synthesizes best practices from Anthropic's official documentation for creating effective Claude Code prompts.

## 🎯 Core Principles

### 1. Be Clear, Direct, and Detailed
> "Think of Claude as a brilliant but very new employee (with amnesia) who needs explicit instructions."

**Key Guidelines:**
- **Give contextual information**: What the task results will be used for, target audience, workflow context
- **Be specific**: If you want only code output, say so explicitly
- **Use sequential steps**: Numbered lists or bullet points for precise execution
- **Show examples**: Demonstrate desired format and behavior

**The Golden Rule:**
> Show your prompt to a colleague with minimal context. If they're confused, Claude will be too.

### 2. Claude 4 Specific Optimizations

**Be Explicit with Instructions:**
- Claude 4 responds well to clear, explicit instructions
- Be specific about desired output to enhance results
- Add modifiers that encourage quality and detail

**Add Context to Improve Performance:**
- Provide motivation behind instructions
- Explain why specific behaviors are important
- Help Claude understand your goals

**Example:**
```
❌ NEVER use ellipses
✅ Your response will be read aloud by text-to-speech, so never use ellipses since the engine won't know how to pronounce them.
```

## 🔧 Technical Best Practices

### 1. Optimize for Parallel Tool Calling
Claude 4 excels at parallel tool execution. Use this prompt for ~100% success rate:

```
For maximum efficiency, whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially.
```

### 2. Leverage Thinking Capabilities
Guide Claude's reasoning for complex tasks:

```
After receiving tool results, carefully reflect on their quality and determine optimal next steps before proceeding. Use your thinking to plan and iterate based on this new information.
```

### 3. Control Output Formatting
Effective strategies for Claude 4:

1. **Tell Claude what to do, not what not to do**
   - Instead of: "Do not use markdown"
   - Try: "Your response should be smoothly flowing prose paragraphs"

2. **Use XML format indicators**
   ```xml
   Write prose sections in <smoothly_flowing_prose_paragraphs> tags.
   ```

3. **Match prompt style to desired output**
   - Remove markdown from prompts to reduce markdown in output

### 4. Enhance Code Generation
For frontend and complex code:

```
Don't hold back. Give it your all. Include as many relevant features and interactions as possible. Add thoughtful details like hover states, transitions, and micro-interactions.
```

## 📋 Prompt Engineering Hierarchy

Follow this order when optimizing prompts:

1. **[Be clear and direct](../../anthropic-md/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct.md)**
2. **[Use examples (multishot)](../../anthropic-md/en/docs/build-with-claude/prompt-engineering/multishot-prompting.md)**
3. **[Let Claude think (chain of thought)](../../anthropic-md/en/docs/build-with-claude/prompt-engineering/chain-of-thought.md)**
4. **[Use XML tags](../../anthropic-md/en/docs/build-with-claude/prompt-engineering/use-xml-tags.md)**
5. **[Give Claude a role (system prompts)](../../anthropic-md/en/docs/build-with-claude/prompt-engineering/system-prompts.md)**
6. **[Prefill Claude's response](../../anthropic-md/en/docs/build-with-claude/prompt-engineering/prefill-claudes-response.md)**
7. **[Chain complex prompts](../../anthropic-md/en/docs/build-with-claude/prompt-engineering/chain-prompts.md)**
8. **[Long context tips](../../anthropic-md/en/docs/build-with-claude/prompt-engineering/long-context-tips.md)**

## 🔍 Claude Code Specific Techniques

### 1. Extended Thinking
Most valuable for:
- Planning complex architectural changes
- Debugging intricate issues
- Creating implementation plans
- Understanding complex codebases
- Evaluating tradeoffs

**Trigger deeper thinking:**
- "think" - basic extended thinking
- "think more", "think harder", "think longer" - deeper thinking

### 2. Session Management
```bash
# Continue most recent conversation
claude --continue

# Continue with new prompt in non-interactive mode
claude --continue --print "Continue with my task"

# Resume specific conversation
claude --resume session-id
```

### 3. Custom System Prompts
```bash
# Override system prompt (only with --print)
claude -p "Build a REST API" --system-prompt "You are a senior backend engineer focused on security and performance."

# Append to system prompt
claude -p "Build API" --append-system-prompt "After writing code, review yourself for security issues."
```

## 📊 Evaluation Best Practices

### Success Criteria Framework
Good criteria are:
- **Specific**: Clear definition of desired achievement
- **Measurable**: Quantitative metrics or well-defined qualitative scales
- **Achievable**: Based on industry benchmarks and model capabilities
- **Relevant**: Aligned with application purpose and user needs

### Evaluation Methods (in order of preference)
1. **Code-based grading**: Fastest, most reliable, extremely scalable
   ```python
   # Exact match
   output == golden_answer
   
   # String match
   key_phrase in output
   ```

2. **LLM-based grading**: Fast, flexible, scalable for complex judgment
   ```python
   def grade_completion(output, rubric):
       prompt = f"Grade based on rubric: {rubric}\nOutput: {output}"
       return llm_evaluate(prompt)
   ```

3. **Human grading**: Most flexible but slow and expensive (avoid if possible)

### LLM Grading Best Practices
- **Detailed rubrics**: "Must mention 'Acme Inc.' in first sentence"
- **Empirical output**: Only 'correct'/'incorrect' or 1-5 scale
- **Encourage reasoning**: Ask LLM to think first, then discard reasoning

## 🚀 Claude Code SDK Integration

### Basic Usage Patterns
```python
# Python SDK
import anyio
from claude_code_sdk import query, ClaudeCodeOptions

async def main():
    async for message in query(
        prompt="Analyze this codebase architecture",
        options=ClaudeCodeOptions(
            max_turns=3,
            system_prompt="You are a senior architect",
            allowed_tools=["Read", "Glob", "Grep"]
        )
    ):
        print(message)
```

### Command Line Optimization
```bash
# JSON output for parsing
claude -p "Analyze code" --output-format json

# Streaming for real-time feedback  
claude -p "Generate tests" --output-format stream-json

# Custom tools and permissions
claude -p "Deploy app" --allowedTools "Bash,Read" --permission-mode acceptEdits
```

## 📝 Template Applications

### Base Template Example
```markdown
You are analyzing a codebase to provide an architectural overview.

Context: This analysis will be used for onboarding new team members.

Instructions:
1. Examine the project structure and identify main components
2. Describe the overall architecture pattern (MVC, microservices, etc.)
3. List key technologies and frameworks used
4. Highlight important files and directories
5. Note any unusual or noteworthy design decisions

Output format: Structured markdown with clear sections and bullet points.
```

### Enhanced Template with Examples
```markdown
[Base template content...]

Examples:

Input: React e-commerce application
Output:
## Architecture Overview
- **Pattern**: Component-based SPA with Redux state management
- **Technologies**: React 18, Redux Toolkit, Material-UI
- **Key Components**: 
  - `/src/components/` - Reusable UI components
  - `/src/pages/` - Route-level components
  - `/src/store/` - Redux state management

Input: Express.js API server
Output:
## Architecture Overview  
- **Pattern**: RESTful API with layered architecture
- **Technologies**: Node.js, Express, PostgreSQL, JWT
- **Key Components**:
  - `/routes/` - API endpoint definitions
  - `/models/` - Database models and schemas
  - `/middleware/` - Authentication and validation
```

## 🔄 Continuous Improvement

### Testing Loop
1. **Define success criteria** for your specific use case
2. **Create test cases** including edge cases
3. **Run evaluations** on prompt variants
4. **Analyze results** and failure modes
5. **Refine prompts** based on insights
6. **Re-test and validate** improvements

### Best Practices for Production
- **Regular evaluation** of prompt performance
- **Version control** for prompt iterations
- **A/B testing** for significant changes
- **Monitoring** for performance degradation
- **Documentation** of learnings and decisions

## 🔗 References

- [Anthropic Prompt Engineering Guide](../../anthropic-md/en/docs/build-with-claude/prompt-engineering/overview.md)
- [Claude 4 Best Practices](../../anthropic-md/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices.md)
- [Claude Code SDK Documentation](../../anthropic-md/en/docs/claude-code/sdk.md)
- [Evaluation Framework](../../anthropic-md/en/docs/test-and-evaluate/develop-tests.md)

---

*This guide synthesizes official Anthropic documentation into actionable best practices for Claude Code prompt development.*