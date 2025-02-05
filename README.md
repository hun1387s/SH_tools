## 개인 RigTool

Maya에서 사용하는 개인 RigTool입니다.



## 사용법

1. `setup.py` 3번 line에 이 코드 경로를 넣는다.

2. `setup.py`를 스크립트창에 던져, 스크립트를 `shelf`에 등록해 사용한다.



# 기능

## Rigging tab

#### DLA on off

- 선택한 obj의 `local axis on off`

#### Joint Visible on off

- viewport상 show탭에서 `joint on off`

#### Joint Black Color

- joint 색상 검은색으로 변경

#### IK FK Blend(T,R,S)

- IK, FK, Set joint 순으로 선택하고 실행
- Translate, Rotate, Scale Blend생성

#### Hierarchy

- 선택한 obj의 하위 계층 모두 선택

#### Parent Cmd

- 선택한 obj 순서대로 자식으로 순차적 `Parent`

#### Snap

- 두번째 선택한 obj를 첫번째 선택한 obj에 붙인다

#### Copy Skin Bone

- 두 Geo를 선택하고 실행
- 첫번째 선택한 Geo의 skin joint를 두번째 선택한 Geo에 bind skin하고,
  weight를 복사해 붙여넣는다.

#### Center Joint

- 선택한 물체의 가운데에 joint를 생성

#### Vertex Joint

- 선택한 Vertex에 각각의 Joint 생성

#### Freeze Joint

- 선택한 Joint를 freeze하는 기능
- bind가 진행된 joint도 사용 가능

#### Pre Rig

- joint의 위치 변경 시, Geo 선택 후 실행
- 원래의 Geo 모양,위치로 돌아간다

#### Joint Draw Style

- 선택한 joint의 `draw style` 설정

#### Joint Divide

- 부모와 자식 joint 선택 후 실행
- 적힌 개수로 나눠 준다.

#### SuffixGrp

- 선택한 obj에 `[작성란]`의 이름으로 offset Grp을 생성한다

#### FK Ctrl

- 선택한 obj에 circle Ctrl shape을 만들어 넣는다.

#### pin box Ctrl

- 선택한 obj에 sphere, box Ctrl shape을 만들어 넣는다.



## Optimize tab

#### Delete Keyframe

- 해당 파일 내에 애니메이션 키를 삭제

#### Delete virus
- 해당 파일 내에 중국 바이러스 노드 삭제

#### Delete Unknown Node

- 해당 파일 내에 알 수 없는 노드 삭제
- 설치 되지 않은 플러그인 관련 노드 삭제

#### Delete Unused Node
- 해당 파일 내에 사용하지 않는 노드 삭제

#### Visible History - Invisible History
- 선택 한 노드를 channelBox의 input 또는 output에 표시 되거나 되지 않도록 설정

#### Cut Attr

- 선택한 attr을 잘라낸다.

#### Copy Attr

- 선택한 attr을 복사한다.

#### Paste Attr

- Cut or Copy한 attr을 붙여넣는다.

#### Add Divider Attr

- ChannelBox에 나눔줄을 생성

#### Move Up Attr

- 선택한 Attr을 위로 한칸 조정

#### Move Down Attr

- 선택한 Attr을 아래로 한칸 조정