.value.mainUnit
| del(.version, .controllerNotes, .mainNotes, .instanceFx)
| del(.stayActiveWhenProjectInBackground, .livesOnUpperFloor)
| del(.activeControllerId, .activeMainPresetId)
| del(.id, .name, .controlDeviceId)
| del(.groups, .defaultGroup, .controllerGroups, .defaultControllerGroup)
| del(.parameters)
| {
  mappings: .mappings | map(
    .
    | del(
      .source.category, # Virtual

      .source.buttonIndex, # 0
      .source.buttonDesign, # { "background": { "kind": "Color" }, "foreground": { "kind": "None" }, "static_text": "" }

      .target.learnable, # false

      .target.fxAnchor, # "id"
      .target.mouseAction, # { "kind": "MoveTo", "axis": "X" }
      .target.takeMappingSnapshot, # { "kind": "ById", "id": "" }
      .target.useTrackGrouping, # false
      .target.useSelectionGanging # false
    )
    | .
  ) | group_by(.source.controlElementIndex) | map({ (.[0].source.controlElementIndex): { mappings: . } }) | add ,
  controllerMappings: .controllerMappings | map(
    select(.controlIsEnabled != false)
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
  ) | group_by(.target.controlElementIndex) | map({ (.[0].target.controlElementIndex): { controllerMappings: . } }) | add
}
| .controllerMappings | to_entries | map(. | select((.value.controllerMappings | length) > 0))
#| map(.controllerMappings)
#| select((.value.controllerMappings | length) > 1)
# | select((.controllerMappings | length) > 0)
# | .mappings * .controllerMappings | .zoom
