# Veritru Orchestrator Service

This service acts as the main API gateway and orchestration layer for the Veritru image analysis platform. It provides:

1. **API Gateway** - NGINX-based reverse proxy routing requests to three core microservices
2. **Dataset Generator** - Processes images through multiple services and generates ML training datasets
3. **Comprehensive Test Suite** - Production-ready testing framework for validating all services

## Project Structure

```
.
├── dataset_generator/
│   ├── dataset_generator.py   # Main Python script for processing images
│   ├── config.yaml            # Configuration file for the service
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Dockerfile for the service
├── tests/                     # Comprehensive test suite
│   ├── test_runner.py         # CLI entry point
│   ├── orchestrator_test.py   # Main orchestration logic
│   ├── clients/               # Service client modules
│   ├── collectors/            # Result aggregation
│   ├── reporters/             # Report generation (CSV, JSON, Markdown)
│   ├── config/                # Test configuration
│   └── README.md              # Test suite documentation
├── docker-compose.yml         # Docker Compose configuration
├── prometheus.yml             # Prometheus configuration
├── nginx.conf                 # NGINX configuration for API Gateway
├── start.sh / mac_start.sh    # Startup scripts
├── e2e_test.sh                # Legacy end-to-end test (deprecated)
└── README.md                  # This file
```

## Core Microservices

The orchestrator integrates with three external Veritru services:

1. **ML Image Service (Josh's)** - Port 5003
   - Deep learning-based image comparison using 9 models (CLIP, ViT, DINO, DinoV2, AIM, BEIT, DEIT, XCIT, SWIN)
   - Async job processing with Redis queues
   - Model-specific worker pools

2. **Non-AI Service (Ella's)** - Port 5002
   - Perceptual hashing (pHash, aHash, dHash, crop-resistant hash)
   - Structural difference detection
   - Hamming distance calculations

3. **Alteration Service (Kiernan's)** - Port 5001
   - Image modifications (rotate, contrast, blur, grayscale, invert, sharpen, noise)
   - Configurable alteration parameters
   - Batch processing support

## Infrastructure Services

4. **API Gateway (NGINX)** - Port 8080
   - Routes requests to appropriate backend services
   - Hardcoded test-key authentication
   - Health checks and monitoring

5. **Redis** - For caching and message queuing
6. **Prometheus** - For metrics collection
7. **Grafana** - For metrics visualization

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.8 or higher (for local development)

### Setup

1. Run the startup script to organize project files:

```bash
chmod +x start.sh
./start.sh
```

2. Place your input images in a directory (default: `sample_images/`)

3. Update the `config.yaml` file with your desired parameters

4. Start the services:

```bash
docker-compose up -d
```

### Using the Dataset Generator

The Dataset Generator service will:

1. Process each input image through Ella's and Josh's services
2. Apply modifications as specified in `config.yaml`
3. Process each modified image through Ella's and Josh's services again
4. Write all results to a CSV file
5. Save all original and modified images to the output directory

### Configuration Options

The `config.yaml` file supports the following options:

- `input_dir`: Directory containing input images
- `output_path`: Output path for dataset (local or GCS bucket)
- `dataset_name`: Name of the dataset
- `max_retries`: Maximum number of retries for service calls
- `modification_params`: List of modification parameters

You can also provide these options via command line arguments:

```bash
python dataset_generator.py --max-count 10 --percentage 50 --random-seed 42
```

## Development

### Adding New Services

To add a new service, update the following files:

1. `docker-compose.yml` - Add the new service configuration
2. `dataset_generator.py` - Add code to process images with the new service
3. `config.yaml` - Add the new service endpoint and any related parameters

## Testing

### Comprehensive Test Suite

The project includes a production-ready test suite for validating all three services:

**Quick Start:**
```bash
cd tests
pip install -r requirements.txt
./quick_test.sh
```

**Manual Run:**
```bash
cd tests
python test_runner.py
```

**Features:**
- ✅ Two-pass testing workflow (original + altered images)
- ✅ Self and cross-image comparisons
- ✅ Parallel execution across all services
- ✅ Comprehensive reporting (CSV, JSON, Markdown)
- ✅ Alteration detection effectiveness analysis
- ✅ Configurable via YAML

**Documentation:**
- `tests/README.md` - Complete test suite guide
- `tests/QUICK_REFERENCE.md` - Command cheat sheet
- `TEST_SUITE_OVERVIEW.md` - Implementation details

**Example output:**
```
test_output/reports/
├── test_summary.md         # Human-readable summary
├── pass1_ml_results.csv    # Pass 1 ML comparisons
├── pass2_ml_results.csv    # Pass 2 ML comparisons
├── pass_comparison.csv     # Pass 1 vs Pass 2 metrics
└── full_report.json        # Complete structured data
```

### Dataset Generator Unit Tests

```bash
cd dataset_generator
python3 -m unittest discover tests
```

## Monitoring

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin_password)
- **API Gateway**: http://localhost:8080

Each service exposes metrics at `/api/v1/metrics` endpoint.

## Requirements Implementation

This project implements the following requirements:

- DEV-101: Integration with Ella's Service
- DEV-102: Integration with Josh's Service
- DEV-103: Integration with Kiernan's Service with Modifications
- DEV-104: Re-run Modified Images Through Ella & Josh
- DEV-105: Record Results to CSV with Modification Flag
- DEV-106: Write Processed Images to Output Path
- DEV-107: Parameterize Dataset Size & Sampling
- DEV-108: CLI & Config Validation