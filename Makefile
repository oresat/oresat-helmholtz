TARGET_DIR := /run/media/$(USER)/CIRCUITPY
BUILD_DIR  := build
SRC_DIR := src
VPATH := $(SRC_DIR)/helmholtz_cage

MPY_EXLUDES := main.py boot.py
PY_SRCS := $(filter-out $(foreach f, $(MPY_EXLUDES), %/$(f)), $(shell find $(VPATH) -type f -name '*.py'))
MPY_OUTS := $(patsubst %.py, $(BUILD_DIR)/%.mpy, $(notdir $(PY_SRCS)))
PRECOMPILED_LIBS := $(filter-out $(VPATH), $(shell find src/* -type d))

.PHONY: all flash clean check-mpy-cross check-board

all: check-mpy-cross $(MPY_OUTS)

$(BUILD_DIR)/%.mpy: %.py | $(BUILD_DIR)
	mpy-cross $< -o $@

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

flash: all check-board
	@echo -e "Copying main.py to $(TARGET_DIR)"
	@cp $(VPATH)/main.py $(TARGET_DIR)
	@echo -e "Copying boot.py to $(TARGET_DIR)"
	@cp $(VPATH)/boot.py $(TARGET_DIR)

	@for dir in $(PRECOMPILED_LIBS); do \
		echo -e "Copying $$dir to $(TARGET_DIR)/lib"; \
		cp -r $$dir $(TARGET_DIR)/lib; \
	done
	@for file in $(BUILD_DIR)/*.mpy; do \
		echo -e "Copying $$file to $(TARGET_DIR)/lib"; \
		cp $$file $(TARGET_DIR)/lib; \
	done
	@echo "Syncing..."
	@sync
	@echo -e "Done"

check-mpy-cross:
	@command -v mpy-cross >/dev/null 2>&1 || \
		{ echo -e "Error: Circuitpython's mpy-cross must be installed" >&2; exit 1; }

check-board:
	@[ -d "$(TARGET_DIR)" ] || \
		{ echo -e "Error: Board not found" >&2; exit 1; }

clean:
	-rm -rf $(BUILD_DIR)
