# Digital Signal Encoder and Decoder

A Python-based project that demonstrates digital data generation, line coding, scrambling, decoding, and Pulse Code Modulation (PCM).

## Features

### 1. Digital Data Generation
- Generate random binary sequences.
- Generate binary sequences containing consecutive zeros.
- Find the longest palindromic substring in a binary sequence.

### 2. Line Coding
Supports the following encoding schemes:
- NRZ-L (Non-Return-to-Zero-Level)
- NRZ-I (Non-Return-to-Zero-Invert)
- Manchester encoding
- Differential Manchester encoding
- AMI (Alternate Mark Inversion)

### 3. Signal Scrambling
Implements:
- AMI encoding
- B8ZS (Bipolar with 8-Zero Substitution)
- HDB3 (High-Density Bipolar-3 Zeros)

These techniques help address long sequences of zeros in digital transmission.

### 4. Signal Decoding
Decoders are implemented for NRZ-L, NRZ-I, Manchester, Differential Manchester, AMI, B8ZS, and HDB3.

### 5. Pulse Code Modulation (PCM)
- Quantize input sample amplitudes.
- Convert quantized samples into binary codewords.
- Decode PCM codewords into reconstructed sample values.
- Support configurable bit depths from 1 to 16 bits per sample.

### 6. Interactive Command-Line Interface
The application provides menu-based access to data generation, encoding, decoding, and PCM operations.

## Technologies Used

- Python
- Matplotlib for signal visualization
- `unittest` for automated testing
- Git and GitHub for version control

## Project Structure

```text
digital-signal-encoder-decoder/
├── src/
│   ├── main.py
│   ├── data_generator.py
│   ├── line_coding.py
│   ├── scrambling.py
│   ├── decoder.py
│   ├── pcm.py
│   ├── delta_modulation.py
│   ├── plotting.py
│   └── utils.py
├── tests/
│   ├── test_data_generator.py
│   ├── test_line_coding.py
│   ├── test_scrambling.py
│   ├── test_decoder.py
│   └── test_pcm.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/samiksha-aaa/digital-signal-encoder-decoder.git
   cd digital-signal-encoder-decoder
   ```

2. Create and activate a virtual environment.

   On Windows PowerShell:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the Application

```bash
python -m src.main
```

Follow the on-screen instructions to select an operation.

## Run Tests

```bash
python -m unittest discover -s tests -v
```

The current test suite passes **58 tests**, covering data generation, line coding, scrambling, decoding, and PCM functionality.

## Learning Objectives

This project demonstrates practical concepts from digital communication, including binary data generation, digital line coding, bipolar scrambling, signal reconstruction, quantization, and binary representation of sampled signals.

## Author

Developed as an academic project on digital signal encoding and decoding.
