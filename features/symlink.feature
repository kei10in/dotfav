Feature: symlink

  Scenario: symlink sub command do nothing if there are no files
    Given there are dotfiles home directory in dotfiles
    And dotfiles home directory contains no files
    When we run dotfav symlink
    Then no files are symlinked

  Scenario: symlink file
    Given there are dotfiles home directory in dotfiles
    And dotfiles home directory contains a file
    When we run dotfav symlink
    Then dotfav symlink creates a symlinked file

  Scenario: symlink directory
    Given there are dotfiles home directory in dotfiles
    And dotfiles home directory contains a directory
    When we run dotfav symlink
    Then dotfav symlink creates a symlinked directory

  Scenario: symlink with config file
    Given there are dotfiles home directory in dotfiles
    And dotfiles contains config file
      '''
      [{ "os": ["darwin"], "target": {"file": "file.darwin"} }]
      '''
    And dotfiles home directory contains a file named "file.darwin"
    When we run dotfav symlink at platform "darwin"
    Then dotfav symlink creates a symlink "file.darwin" to "file"
