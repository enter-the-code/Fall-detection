# Documentation
발표 자료 및 조사 내용을 정리한 자료를 업로드하는 공간입니다
## Upload Rules
* 가급적이면 docs 브랜치 사용하여 업로드 후 PR
* 용량을 줄이기 위해서, 재사용 할 이미지는 별도 폴더에 나눠 저장
* ppt 파일은 이미지를 제거한 상태로, 원본 자료는 pdf로 저장

## Rebase Policy
PR 통한 rebase 이후 해당 branch 계속하여 사용할 시, main으로부터 merge 필요
```bash
git checkout branch_name
git merge main
git push origin branch_name
```