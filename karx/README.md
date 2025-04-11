# KARX - AI Code Assistant

KARX is an intelligent code assistant that helps developers write, maintain, and understand code more efficiently. It combines multiple AI agents to provide a comprehensive development experience.

## Features

1. **Autonomous Code Generator**
   - Parse prompts from files or clipboard
   - Create complete project structures
   - Follow clean code practices

2. **Code Memory**
   - Track files, functions, and variables
   - Persistent storage in code_map.json
   - Smart suggestions based on history

3. **Multi-Agent System**
   - CodeWriter: Generate code from prompts
   - SmartFix: Detect and fix common errors
   - Explainer: Line-by-line code explanation
   - Linker: Fix import paths

4. **Resource Guardian**
   - Monitor system resources
   - Prevent performance issues
   - Automatic throttling

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/karx.git
   cd karx
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

```bash
# Generate code from a prompt
python main.py generate "Create a web server" --output ./output

# Fix code issues
python main.py fix path/to/file.py

# Get code explanation
python main.py explain path/to/file.py

# Fix import paths
python main.py imports path/to/file.py

# Watch clipboard for prompts
python main.py watch
```

## Project Structure

```
karx/
├── main.py                 # Main CLI interface
├── core/                   # Core AI agents
│   ├── code_writer.py
│   ├── smartfix.py
│   ├── explainer.py
│   ├── linker.py
├── memory/                 # Code memory management
│   ├── code_map.json
│   └── memory_manager.py
├── monitor/               # Resource monitoring
│   └── guardian_angel.py
├── clipboard/            # Clipboard integration
│   └── clipboard_listener.py
├── utils/                # Helper utilities
│   └── helpers.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 