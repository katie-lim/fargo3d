---

database-plugin: basic

---

<%%
name: simulations
description: list of simulations
columns:
  __file__:
    key: __file__
    input: markdown
    label: File
    accessor: __file__
    isMetadata: true
    skipPersist: false
    isDragDisabled: false
    csvCandidate: true
    position: 1
    isSorted: true
    isSortedDesc: false
    config:
      enable_media_view: true
      media_width: 100
      media_height: 100
      isInline: true
      source_data: current_folder
  status:
    input: select
    key: status
    accessor: status
    label: status
    position: 2
    options:
      - { label: "Not running", backgroundColor: "hsl(1, 95%, 90%)"}
      - { label: "Queuing", backgroundColor: "hsl(243.67346938775506,96.07843137254903%,90%)"}
      - { label: "Running", backgroundColor: "hsl(202, 95%, 90%)"}
      - { label: "Finished", backgroundColor: "hsl(136, 95%, 90%)"}
    config:
      enable_media_view: true
      media_width: 100
      media_height: 100
      isInline: false
  period_ratio:
    input: text
    accessor: period_ratio
    key: period_ratio
    label: period ratio
    position: 6
    config:
      enable_media_view: true
      media_width: 100
      media_height: 100
      isInline: true
      source_data: current_folder
  suggested_resonance:
    input: select
    accessor: suggested_resonance
    key: suggested_resonance
    label: suggested resonance
    position: 7
    options:
      - { label: "2:1", backgroundColor: "hsl(193.48469578942587,95.00000000000011%,90%)"}
      - { label: "3:2", backgroundColor: "hsl(103, 95%, 90%)"}
      - { label: "5:3", backgroundColor: "hsl(40.69399811500729,95.00000000000011%,90%)"}
    config:
      enable_media_view: true
      media_width: 100
      media_height: 100
      isInline: true
      source_data: current_folder
  resonant_angles_plot:
    input: text
    accessor: resonant_angles_plot
    key: resonant_angles_plot
    label: resonant angles plot
    position: 9
    config:
      enable_media_view: true
      media_width: 100
      media_height: 100
      isInline: true
      source_data: current_folder
  period_ratio_plot:
    input: text
    accessor: period_ratio_plot
    key: period_ratio_plot
    label: period ratio plot
    position: 8
    config:
      enable_media_view: true
      media_width: 100
      media_height: 100
      isInline: true
      source_data: current_folder
  eccentricity_plot:
    input: text
    accessor: eccentricity_plot
    key: eccentricity_plot
    label: eccentricity plot
    position: 10
    config:
      enable_media_view: true
      media_width: 100
      media_height: 100
      isInline: true
      source_data: current_folder
  gas_density_plot:
    input: text
    accessor: gas_density_plot
    key: gas_density_plot
    label: gas density plot
    position: 13
    config:
      enable_media_view: true
      media_width: 100
      media_height: 100
      isInline: true
      source_data: current_folder
  notes:
    input: text
    accessor: notes
    key: notes
    label: notes
    position: 4
    config:
      enable_media_view: true
      media_width: 100
      media_height: 100
      isInline: true
      source_data: current_folder
  e1:
    input: text
    accessor: e1
    key: e1
    label: e1
    position: 11
    config:
      enable_media_view: true
      media_width: 100
      media_height: 100
      isInline: true
      source_data: current_folder
  e2:
    input: text
    accessor: e2
    key: e2
    label: e2
    position: 12
    config:
      enable_media_view: true
      media_width: 100
      media_height: 100
      isInline: true
      source_data: current_folder
  semi_major_axes_plot:
    input: text
    accessor: semi_major_axes_plot
    key: semi_major_axes_plot
    label: semi major axes plot
    position: 5
    config:
      enable_media_view: true
      media_width: 100
      media_height: 100
      isInline: true
      source_data: current_folder
  azimuthally_avged_surface_density_plot:
    input: text
    accessor: azimuthally_avged_surface_density_plot
    key: azimuthally_avged_surface_density_plot
    label: azimuthally avged surface density plot
    position: 14
    config:
      enable_media_view: false
      media_width: 100
      media_height: 100
      isInline: true
      source_data: current_folder
  tags:
    input: tags
    accessor: tags
    key: tags
    label: tags
    position: 3
    options:
      - { label: "photoevaporation", backgroundColor: "hsl(154.861876021984,95.00000000000011%,90%)"}
      - { label: "review", backgroundColor: "hsl(27.88508925327025,35.768735219255774%,77.658855%)"}
      - { label: "fixed inner planet", backgroundColor: "hsl(219.34229651162786,95.00000000000011%,90%)"}
      - { label: "data loss", backgroundColor: "hsl(333, 95%, 90%)"}
      - { label: "fixed data loss", backgroundColor: "hsl(163, 95%, 90%)"}
    config:
      enable_media_view: true
      media_width: 100
      media_height: 100
      isInline: false
      source_data: current_folder
  __modified__:
    key: __modified__
    input: calendar_time
    label: Modified
    accessor: __modified__
    isMetadata: true
    isDragDisabled: false
    skipPersist: false
    csvCandidate: true
    isSorted: false
    isSortedDesc: false
    config:
      enable_media_view: true
      media_width: 100
      media_height: 100
      isInline: false
      source_data: current_folder
config:
  enable_show_state: false
  group_folder_column: 
  remove_field_when_delete_column: false
  cell_size: compact
  sticky_first_column: true
  show_metadata_created: false
  show_metadata_modified: true
  source_data: current_folder
  source_form_result: root
filters:
%%>