.value.mainUnit
| del(.version, .controllerNotes, .mainNotes, .instanceFx)
| del(.stayActiveWhenProjectInBackground, .livesOnUpperFloor)
| del(.activeControllerId, .activeMainPresetId)
| del(.id, .name, .controlDeviceId)
| del(.groups, .defaultGroup, .controllerGroups, .defaultControllerGroup)
| del(.parameters)
| del(.controllerMappings)
| .mappings
| map(
  .
  | del(
    .source.category, # Virtual
    .source.buttonIndex, # 0
    .source.buttonDesign, # { "background": { "kind": "Color" }, "foreground": { "kind": "None" }, "static_text": "" }
    .target.fxAnchor, # "id"
    .target.mouseAction, # { "kind": "MoveTo", "axis": "X" }
    .target.learnable, # false
    .target.takeMappingSnapshot, # { "kind": "ById", "id": "" }
    .target.useTrackGrouping, # false
    .target.useSelectionGanging # false
  )
  | .
)
