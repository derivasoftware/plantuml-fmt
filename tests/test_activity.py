"""Activity blocks and sequence lifecycle blocks indent like frames (grammar 0.10)."""

from plantuml_fmt.formatter import format_text

ACTIVITY = """@startuml
start
if (ok?) then (yes)
:a;
elseif (maybe?) then
:b;
else (no)
:c;
endif
while (more?) is (yes)
:loop;
break
endwhile (no)
repeat :init;
:step;
repeat while (again?)
switch (t)
case (A)
:ca;
case (B)
:cb;
endswitch
fork
:f1;
fork again
fork
:nested;
end fork
end fork {or}
split
:s1;
split again
:s2;
end split
partition Init {
:p;
}
stop
@enduml
"""

ACTIVITY_CANON = """@startuml
start
if (ok?) then (yes)
  :a;
elseif (maybe?) then
  :b;
else (no)
  :c;
endif
while (more?) is (yes)
  :loop;
  break
endwhile (no)
repeat :init;
  :step;
repeat while (again?)
switch (t)
case (A)
  :ca;
case (B)
  :cb;
endswitch
fork
  :f1;
fork again
  fork
    :nested;
  end fork
end fork {or}
split
  :s1;
split again
  :s2;
end split
partition Init {
  :p;
}
stop
@enduml
"""

LIFECYCLE = """@startuml
box "Kitchen" #LightBlue
participant Bob
actor Al
end box
ref over Bob, Al
  keep   this   text
end ref
alt ok
Bob -> Al
end
@enduml
"""

LIFECYCLE_CANON = """@startuml
box "Kitchen" #LightBlue
  participant Bob
  actor Al
end box
ref over Bob, Al
  keep   this   text
end ref
alt ok
  Bob -> Al
end
@enduml
"""


def test_activity_blocks_indent_and_clauses_align_with_their_opener():
    assert format_text(ACTIVITY) == ACTIVITY_CANON


def test_activity_formatting_is_idempotent():
    assert format_text(ACTIVITY_CANON) == ACTIVITY_CANON


def test_box_indents_and_reference_body_is_frozen():
    assert format_text(LIFECYCLE) == LIFECYCLE_CANON
    assert format_text(LIFECYCLE_CANON) == LIFECYCLE_CANON
