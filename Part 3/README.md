# 🖥️ Bash System Toolkit

A collection of modular Bash scripts designed to analyze system information, customize terminal output, and perform deep file system inspection.

This project demonstrates practical shell scripting techniques including input validation, system monitoring, formatting, and automation.

---

## 📦 Project Structure

```
src/
 ├── 01/   # Basic parameter validation
 ├── 02/   # System information
 ├── 03/   # Colored output (CLI args)
 ├── 04/   # Colored output (config file)
 └── 05/   # File system analysis
```

Each folder contains:
- `main.sh` – main entry point
- Additional helper scripts (modular structure)

---

## ⚙️ Features Overview

### 1. Input Validation Script
- Accepts a single parameter
- Prints the parameter if it's text
- Rejects numeric input with an error message

---

### 2. System Information Script
Displays detailed system information:

- Hostname
- Timezone
- Current user
- OS name and version
- Current date and time
- System uptime (human-readable + seconds)
- Network information (IP, mask, gateway)
- RAM usage (total / used / free)
- Disk usage for root partition

#### Additional Feature
- Prompts user to save output into a timestamped `.status` file

---

### 3. Colored Output (Arguments)
Customize output appearance using CLI parameters:

```
./main.sh <bg_name> <font_name> <bg_value> <font_value>
```

Color codes:

| Code | Color  |
|------|--------|
| 1    | White  |
| 2    | Red    |
| 3    | Green  |
| 4    | Blue   |
| 5    | Purple |
| 6    | Black  |

#### Rules:
- Background and font colors must not match
- Invalid combinations will stop execution with explanation

---

### 4. Colored Output (Config File)
Same functionality as Part 3, but using a configuration file instead of CLI arguments.

#### Example config:
```
column1_background=2
column1_font_color=4
column2_background=5
column2_font_color=1
```

#### Features:
- Uses default colors if values are missing
- Prints the active color scheme after execution

---

### 5. File System Analyzer
Analyzes a given directory (must end with `/`):

```
./main.sh /path/to/directory/
```

#### Output includes:

- Total number of folders (including nested)
- Top 5 largest folders
- Total number of files
- File type breakdown:
  - Configuration (.conf)
  - Text files
  - Executables
  - Log files (.log)
  - Archives
  - Symbolic links

- Top 10 largest files (path, size, type)
- Top 10 largest executable files (path, size, MD5 hash)
- Script execution time

---

## 🚀 How to Run

1. Clone repository:
```
git clone <your-repo-link>
cd <repo>
```

2. Give execution permission:
```
chmod +x src/*/main.sh
```

3. Run scripts:

### Example:
```
cd src/02
./main.sh
```

---

## 🧠 Key Concepts Used

- Bash scripting best practices
- Modular script design
- Input validation
- System utilities (`top`, `df`, `free`, `ip`, `uptime`)
- Text processing (`awk`, `grep`, `sed`)
- File system traversal (`find`, `du`)
- Hash generation (`md5sum`)

---

## 📌 Requirements

- Linux environment (tested on Ubuntu Server)
- Bash shell
- Standard GNU utilities

---

## 💡 Notes

- Scripts are designed to be simple, readable, and extendable
- All outputs are formatted for clarity
- Error handling is implemented for incorrect input

---

## 📬 Contribution

Feel free to fork, improve, or adapt these scripts for your own system automation tasks.

---

## 📄 License

This project is open-source and available for educational and personal use.

