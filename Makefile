# DarknessMUD Makefile

.PHONY: help lint clean build run purge stop repair

# Use local gradle home to bypass global cache corruption
LOCAL_GRADLE_HOME := .gradle_home
GRADLE_OPTS := --gradle-user-home $(LOCAL_GRADLE_HOME) --no-daemon --stacktrace

# Automatically detect Gradle
GRADLE_BIN := $(shell [ -f ./gradlew ] && echo ./gradlew || echo gradle)
GRADLE := $(GRADLE_BIN) $(GRADLE_OPTS)

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

lint: stop ## Run static analysis
	rm -rf build
	$(GRADLE) check

clean: ## Clean build artifacts
	$(GRADLE) clean
	rm -rf build

build: stop ## Build the application
	rm -rf build
	$(GRADLE) build -x test

run: stop ## Run the application (Uses local cache to fix truncation errors)
	rm -rf build
	$(GRADLE) bootRun --refresh-dependencies

repair: stop ## Nuclear option: Wipe everything and rebuild cache
	$(GRADLE) --stop || true
	@pkill -f gradle || true
	rm -rf build .gradle $(LOCAL_GRADLE_HOME)
	@echo "Environment reset. Run 'make run' to rebuild."

stop: ## Force stop the Gradle daemon and kill lingering processes
	$(GRADLE_BIN) --stop || true
	@pkill -f java || true
	@pkill -f gradle || true

test: stop ## Run unit tests
	rm -rf build
	$(GRADLE) test
