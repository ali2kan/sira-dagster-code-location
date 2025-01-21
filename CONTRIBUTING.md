# Contributing to Dagster Core Docker

First off, thank you for considering contributing to this project!

## How to Contribute

1. **Fork the Repository**
   - Create your own fork of the repo
   - Clone it locally

2. **Create a Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow the existing code style
   - Add tests if applicable
   - Update documentation as needed

4. **Test Your Changes**
   - Build the Docker image locally
   - Run basic functionality tests
   - Ensure all existing tests pass

5. **Commit Your Changes**

   ```bash
   git commit -m "feat: add your feature description"
   ```

   - Follow [Conventional Commits](https://www.conventionalcommits.org/)

6. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Use the PR template
   - Describe your changes
   - Link any relevant issues

## Development Setup

1. **Prerequisites**
   - Docker
   - Python 3.12+
   - Docker Buildx for multi-arch builds

2. **Local Development**

   ```bash
   # Build the image
   docker buildx bake -f docker-bake.hcl

   # Run locally
   docker-compose up
   ```

## Code Style

- Follow PEP 8 for Python code
- Use descriptive variable names
- Comment complex logic
- Keep functions focused and small

## Questions?

Feel free to open an issue for any questions or concerns.
