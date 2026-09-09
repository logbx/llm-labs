.PHONY: help validate test clean

help: ## Show this help message
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

validate: ## Run validation checks on the repository
	@python3 validate.py

test: validate ## Alias for validate

clean: ## Clean temporary files and caches
	@echo "Cleaning temporary files..."
	@find . -type f -name "*.tmp" -delete
	@find . -type f -name "*.bak" -delete
	@find . -type f -name "*~" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleaned!"