.value.mainUnit
| ({
  SMALL_STEP: {"minStepSize":0.005,"maxStepSize":1.0,"minStepFactor":1,"maxStepFactor":1},
  MINIMAL_STEP: {"minTargetValue":0.99999,"minStepFactor":1,"maxStepFactor":1,"reverseIsEnabled":true},
  SINGLE_PRESS: {"minStepFactor":1,"maxStepFactor":1,"outOfRangeBehavior":"min","buttonUsage":"press-only"},
  NORMAL: {"minStepFactor":1,"maxStepFactor":1},
  PERCENT: {"minStepFactor":1,"maxStepFactor":100},
  NORMAL_WITH_MAX_STEP: {"maxSourceValue":0.0,"minStepFactor":1,"maxStepFactor":1},
  NORMAL_WITH_MAX_VALUE: {"maxTargetValue":0.00001,"minStepFactor":1,"maxStepFactor":1},
  NORMAL_TURBO: {"minStepFactor":1,"maxStepFactor":1,"turboRate":100,"fireMode":"turbo"},
  RESET_TO_CENTER: {"minTargetValue":0.5,"maxTargetValue":0.5,"minStepFactor":1,"maxStepFactor":1},
  SOURCE_04: {"maxSourceValue":0.4,"minStepFactor":1,"maxStepFactor":1},
  SOURCE_075: {"maxSourceValue":0.75,"minStepFactor":1,"maxStepFactor":1},
  SOURCE_05075: {"minSourceValue":0.05,"maxSourceValue":0.75,"minStepFactor":1,"maxStepFactor":1},
  TOGGLE: {"type":2,"minStepFactor":1,"maxStepFactor":1},
  TOGGLE_LONG: {"type":2,"minStepFactor":1,"maxStepFactor":1,"maxPressMillis":250},
  TOGGLE_LIMITED: {"type":2,"minStepFactor":1,"maxStepFactor":1,"outOfRangeBehavior":"min"},
  TOGGLE_WITH_MIN: {"type":2,"minTargetValue":1.0,"minStepFactor":1,"maxStepFactor":1},
  INC1: {"type":1,"minStepFactor":1,"maxStepFactor":1},
  INC1_REV: {"type":1,"minStepFactor":1,"maxStepFactor":1,"reverseIsEnabled":true},
  INC8: {"type":1,"minStepFactor":8,"maxStepFactor":8},
  INC8_REV: {"type":1,"minStepFactor":8,"maxStepFactor":8,"reverseIsEnabled":true},
  INC1_ROTATE: {"type":1,"minStepFactor":1,"maxStepFactor":1,"rotateIsEnabled":true},
  INC_TURBO1: {"type":1,"minStepFactor":1,"maxStepFactor":1,"turboRate":100,"fireMode":"turbo"},
  INC_TURBO1_REVERSE: {"type":1,"minStepFactor":1,"maxStepFactor":1,"turboRate":100,"reverseIsEnabled":true,"fireMode":"turbo"},
  INC_TURBO1_LONG: {"type":1,"minStepFactor":1,"maxStepFactor":1,"minPressMillis":300,"maxPressMillis":300,"turboRate":60,"fireMode":"turbo"},
  INC_TURBO1_LONG_REVERSE: {"type":1,"minStepFactor":1,"maxStepFactor":1,"minPressMillis":300,"maxPressMillis":300,"turboRate":60,"reverseIsEnabled":true,"fireMode":"turbo"},
  INC_TURBO8: {"type":1,"minStepSize":0.08,"maxStepSize":0.08,"minStepFactor":8,"maxStepFactor":8,"turboRate":100,"fireMode":"turbo"},
  INC_TURBO8_REVERSE: {"type":1,"minStepFactor":8,"maxStepFactor":8,"turboRate":100,"reverseIsEnabled":true,"fireMode":"turbo"},
  INC_TURBO8_LONG: {"type":1,"minStepFactor":8,"maxStepFactor":8,"minPressMillis":300,"maxPressMillis":300,"turboRate":100,"fireMode":"turbo"},
  INC_TURBO8_LONG_REVERSE: {"type":1,"minStepFactor":8,"maxStepFactor":8,"minPressMillis":300,"maxPressMillis":300,"turboRate":100,"reverseIsEnabled":true,"fireMode":"turbo"}
} | to_entries) as $MODES
| del(.version, .controllerNotes, .mainNotes, .instanceFx)
| del(.stayActiveWhenProjectInBackground, .livesOnUpperFloor)
| del(.activeControllerId, .activeMainPresetId)
| del(.id, .name, .controlDeviceId)
| del(.groups, .defaultGroup, .controllerGroups, .defaultControllerGroup)
| del(.parameters)
| {
  mappings: .mappings | map(
    .mode | del(.eelFeedbackTransformation, .feedbackColor, .feedbackType)
  ) | unique,
  controllerMappings: .controllerMappings | map(
    select(.controlIsEnabled != false)
    | . += {mode: (.mode as $CURR | ($MODES | map(select(.value==$CURR).key)[0]))}
    | del(
      .source.buttonIndex, # 0
      .source.buttonDesign, # { "background": { "kind": "Color" }, "foreground": { "kind": "None" }, "static_text": "" }

      .target.category, # Virtual
      .target.pollForFeedback, # false
      .target.seekBehavior, # "Immediate"

      .target.fxAnchor, # "id"
      .target.mouseAction, # { "kind": "MoveTo", "axis": "X" }
      .target.takeMappingSnapshot, # { "kind": "ById", "id": "" }
      .target.useTrackGrouping, # false
      .target.useSelectionGanging # false
    )
    | .
  ) | group_by(.target.controlElementIndex) | map({ (.[0].target.controlElementIndex): .[0] }) | add
}
| .controllerMappings

# | .controllerMappings * .mappings
# | to_entries | map(. | select((.value.mappings | length) > 1))
