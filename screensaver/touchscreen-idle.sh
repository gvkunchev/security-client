#!/bin/bash

DEVICE_DIR="/sys/class/backlight/10-0045"  # Adjust if needed (there should be only one tere)
BRIGHTNESS_FILE="$DEVICE_DIR/brightness"
POWER_FILE="$DEVICE_DIR/bl_power"
MAX_BRIGHTNESS=$(cat "$DEVICE_DIR/max_brightness")

IDLE_TIME=10      # idle before starting fade
FADE_TIME=10     # seconds to fade down
STEPS=20         # how many steps in fade
STEP_DELAY=$((FADE_TIME / STEPS))

fade_pid=0

TOUCH_DEV="event4"  # Adjust if needed (use "dd if=/dev/input/eventX" and start touching the screen to figure out)
TOUCH_PATH="/dev/input/$TOUCH_DEV"

restore_screen() {
    # cancel fade if running
    if [ $fade_pid -ne 0 ] && kill -0 $fade_pid 2>/dev/null; then
        kill $fade_pid 2>/dev/null
        wait $fade_pid 2>/dev/null
        fade_pid=0
    fi
    echo 0 > "$POWER_FILE"
    echo $MAX_BRIGHTNESS > "$BRIGHTNESS_FILE"
}

fade_and_poweroff() {
    (
        sleep $IDLE_TIME

        # check again after sleep
        if [ $(($(date +%s) - last_event)) -lt $IDLE_TIME ]; then
            exit 0
        fi

        current=$(cat "$BRIGHTNESS_FILE")
        step=$((current / STEPS))
        if (( step < 1 )); then step=1; fi

        for ((i=0; i<$STEPS; i++)); do
            # stop fading early if user touched
            if [ $(($(date +%s) - last_event)) -lt $IDLE_TIME ]; then
                exit 0
            fi
            new_brightness=$((current - step * i))
            if (( new_brightness < 1 )); then
                new_brightness=1
            fi
            echo $new_brightness > "$BRIGHTNESS_FILE"
            sleep $STEP_DELAY
        done

        echo 1 > "$POWER_FILE"
    ) &
    fade_pid=$!
}

# Start main loop
libinput debug-events --device "$TOUCH_PATH" | while read -r line; do
    now=$(date +%s)
    last_event=$now
    restore_screen
    fade_and_poweroff
done