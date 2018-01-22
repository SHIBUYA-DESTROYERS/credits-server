# ウェブフロントエンドの方針

## 流れ

1. 学校選択
1. 学科選択（複数選択可）3へは画面遷移なし
1. 科目の履修状況を選択（スイッチみたいなUIで）

## URI

- `/#{school_id}/`

## 使う技術

- localStorageを使いたい

```js
var obj = {
      0001: 1,
      0002: 0
    };
var obj = JSON.stringify(obj);
localStorage.setItem('Key', obj);
```
