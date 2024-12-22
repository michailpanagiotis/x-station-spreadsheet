.value.mainUnit
| ({
  CC: 0,
  NOTE_VELOCITY: 1,
  NOTE_NUMBER: 2,
  PITCH_WHEEL: 3,
  AFTERTOUCH: 4,
  PROGRAM_CHANGE_NUMBER: 5,
  NRPN: 6,
  POLY_AFTERTOUCH: 7
} | to_entries) as $CONTROL_TYPE
| ({
  SMALL_STEP: {"minStepSize":0.005,"maxStepSize":1.0,"minStepFactor":1,"maxStepFactor":1},


  MINIMAL_STEP: {"minTargetValue":0.99999,"minStepFactor":1,"maxStepFactor":1,"reverseIsEnabled":true},
  NORMAL_WITH_MAX_VALUE: {"maxTargetValue":0.00001,"minStepFactor":1,"maxStepFactor":1},


  SINGLE_PRESS: {"minStepFactor":1,"maxStepFactor":1,"outOfRangeBehavior":"min","buttonUsage":"press-only"},
  NORMAL: {"minStepFactor":1,"maxStepFactor":1},
  PERCENT: {"minStepFactor":1,"maxStepFactor":100},
  NORMAL_WITH_MAX_STEP: {"maxSourceValue":0.0,"minStepFactor":1,"maxStepFactor":1},
  NORMAL_CONTINUOUS: {"minStepFactor":1,"maxStepFactor":1,"turboRate":100,"fireMode":"turbo"},
  RESET_TO_CENTER: {"minTargetValue":0.5,"maxTargetValue":0.5,"minStepFactor":1,"maxStepFactor":1},
  SOURCE_04: {"maxSourceValue":0.4,"minStepFactor":1,"maxStepFactor":1},
  SOURCE_075: {"maxSourceValue":0.75,"minStepFactor":1,"maxStepFactor":1},
  SOURCE_05075: {"minSourceValue":0.05,"maxSourceValue":0.75,"minStepFactor":1,"maxStepFactor":1},
  TOGGLE: {"type":2,"minStepFactor":1,"maxStepFactor":1},
  TOGGLE_LONG: {"type":2,"minStepFactor":1,"maxStepFactor":1,"maxPressMillis":250},
  TOGGLE_LIMITED: {"type":2,"minStepFactor":1,"maxStepFactor":1,"outOfRangeBehavior":"min"},
  TOGGLE_WITH_MIN: {"type":2,"minTargetValue":1.0,"minStepFactor":1,"maxStepFactor":1},

  PLUS1: {"type":1,"minStepFactor":1,"maxStepFactor":1},
  PLUS1_LONG: {"type":1,"minStepFactor":1,"maxStepFactor":1,"minPressMillis":300,"maxPressMillis":300,"turboRate":60,"fireMode":"turbo"},
  PLUS8: {"type":1,"minStepFactor":8,"maxStepFactor":8},
  PLUS8_LONG: {"type":1,"minStepFactor":8,"maxStepFactor":8,"minPressMillis":300,"maxPressMillis":300,"turboRate":100,"fireMode":"turbo"},
  MINUS1: {"type":1,"minStepFactor":1,"maxStepFactor":1,"reverseIsEnabled":true},
  MINUS1_LONG: {"type":1,"minStepFactor":1,"maxStepFactor":1,"minPressMillis":300,"maxPressMillis":300,"turboRate":60,"reverseIsEnabled":true,"fireMode":"turbo"},
  MINUS8: {"type":1,"minStepFactor":8,"maxStepFactor":8,"reverseIsEnabled":true},
  MINUS8_LONG: {"type":1,"minStepFactor":8,"maxStepFactor":8,"minPressMillis":300,"maxPressMillis":300,"turboRate":100,"reverseIsEnabled":true,"fireMode":"turbo"},

  INC1_ROTATE: {"type":1,"minStepFactor":1,"maxStepFactor":1,"rotateIsEnabled":true},
  PLUS1_CONTINUOUS: {"type":1,"minStepFactor":1,"maxStepFactor":1,"turboRate":100,"fireMode":"turbo"},
  PLUS8_CONTINUOUS: {"type":1,"minStepSize":0.08,"maxStepSize":0.08,"minStepFactor":8,"maxStepFactor":8,"turboRate":100,"fireMode":"turbo"},

  MINUS1_CONTINUOUS: {"type":1,"minStepFactor":1,"maxStepFactor":1,"turboRate":100,"reverseIsEnabled":true,"fireMode":"turbo"},
  MINUS8_CONTINUOUS: {"type":1,"minStepFactor":8,"maxStepFactor":8,"turboRate":100,"reverseIsEnabled":true,"fireMode":"turbo"}
} | to_entries) as $MODES
| ({
  MOD_1_ON: { "paramIndex": 1, "isOn": true },
  MOD_1_OFF: { "paramIndex": 1, "isOn": false },
  MOD_2_ON: { "paramIndex": 2, "isOn": true },
  MOD_2_OFF: { "paramIndex": 2, "isOn": false }
} | to_entries) as $MODIFIERS
| (.groups | map({ (.id): . }) | add) as $GROUPS
| (.controllerGroups | map({ (.id): . }) | add) as $CONTROLLER_GROUPS
| del(.version, .controllerNotes, .mainNotes, .instanceFx)
| del(.stayActiveWhenProjectInBackground, .livesOnUpperFloor)
| del(.activeControllerId, .activeMainPresetId)
| del(.id, .name, .controlDeviceId)
| del(.groups, .defaultGroup, .controllerGroups, .defaultControllerGroup)
| del(.parameters)
# CONTROLLER
| (.controllerMappings | map({ (.target.controlElementIndex): (
  select(.controlIsEnabled != false)
  | .source += {
    type: ((.source.type as $CURR | ($CONTROL_TYPE | map(select(.value==$CURR).key)[0])) // "CC")
  }
  | del(.source.buttonDesign, .source.buttonIndex, .source.is14Bit)
)}) | add) as $CONTROLS
# MAPPINGS
| .mappings | map(
  .controllerSource = $CONTROLS[.source.controlElementIndex].source
  | select(.controllerSource)
  | del(.source)
  | del(
      .source.buttonDesign, # { "background": { "kind": "Color" }, "foreground": { "kind": "None" }, "static_text": "" }
      .source.buttonIndex, # 0
      .source.is14Bit, # false

      .target.pollForFeedback, # false
      .target.mouseAction, # { "kind": "MoveTo", "axis": "X" }
      .target.takeMappingSnapshot, # { "kind": "ById", "id": "" }
      .target.useTrackGrouping, # false
      .target.useSelectionGanging, # false
      .target.learnable, #false
      .target.seekBehavior, # "ReaperPreference" if mode in (MINIMAL_STEP, NORMAL_WITH_MAX_VALUE) else "Immediate"
      .id,
      .groupId
  )
  | . += {mode: (.mode as $CURR | ($MODES | map(select(.value==$CURR).key)[0]))}
  # | select(.target.seekBehavior == "ReaperPreference")
)
