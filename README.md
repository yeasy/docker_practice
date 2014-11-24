Docker —— 從入門到實踐
===============

v0.2.9

[Docker](docker.com) 是個偉大的項目，它徹底釋放了虛擬化的，讓應用程式的分派、部署和管理都變得前所未有的有效率和輕鬆！

本書既適用於具備基礎 Linux 知識的 Docker 初學者，也可供希望理解原理和實做的進階使用者參考。同時，書中給出的實踐案例，可供在進行實際部署時借鑒。

本書源於 [WaitFish](github.com/qcpm1983) 的《[Docker 學習手冊 v1.0](https://github.com/yeasy/docker_practice/raw/master/_local/docker_manual_waitfish.pdf)》內容。後來，[yeasy](github.com/yeasy)
根據最新 Docker 版本對內容進行了修訂和重寫，並增加內容；經協商將所有內容開源，採用網路合作的方式進行維護。

前六章為基礎內容，供使用者理解 Docker 的基本概念和操作；7 ~ 9 章介紹一些進階操作；第 10 章給出典型的應用場景和實踐案例；11 ~ 13 章介紹關於 Docker 實做的相關技術。

最新版本線上閱讀：[正體版](https://www.gitbook.io/book/philipzheng/docker_practice)、[簡體版](https://www.gitbook.io/book/yeasy/docker_practice) 或 [DockerPool](http://dockerpool.com/static/books/docker_practice/index.html)。

另外，歡迎加入 [Docker.Taipei](https://www.facebook.com/groups/docker.taipei/) 和 [Meetup](http://www.meetup.com/Docker-Taipei/) ，分享 Docker 資源，交流 Docker 技術。


本書原始碼在 Github 上維護，歡迎參與： [https://github.com/philipz/docker_practice](https://github.com/philipz/docker_practice)。

感謝所有的 [貢獻者](https://github.com/philipz/docker_practice/graphs/contributors)。

## 主要版本歷史
* 0.3: 2014-10-TODO
    * 完成倉庫章節；
    * 重寫安全章節；
    * 修正底層實做章節的架構、名字空間、控制組、檔案系統、容器格式等內容；
    * 新增對常見倉庫和鏡像的介紹；
    * 新增 Dockerfile 的介紹；
    * 重新校訂中英文混排格式。
* 0.2: 2014-09-18
    * 對照官方文檔重寫介紹、基本概念、安裝、鏡像、容器、倉庫、資料管理、網路等章節；
    * 新增底層實做章節；
    * 新增命令查詢和資源連結章節；
    * 其它修正。
* 0.1: 2014-09-05
    * 新增基本內容;
    * 修正錯別字和表達不通順的地方。

## 貢獻力量

如果想做出貢獻的話，你可以：

- 幫忙校對，挑錯別字、語病等等
- 提出修改建議
- 提出術語翻譯建議

## 翻譯建議

如果你願意一起校對的話，請仔細閱讀：

- 使用 markdown 進行翻譯，文件名必須使用英文，因為中文的話 gitbook 編譯的時候會出問題
- 引號請使用「」和『』
- fork 過去之後新建一個分支進行翻譯，完成後 pull request 這個分支，沒問題的話我會合併到 master 分支中
- 有其他任何問題都歡迎發 issue，我看到了會盡快回覆

謝謝！

## 關於術語

翻譯術語的時候請參考這個流程：

- 盡量保證與台灣習慣術語和已翻譯的內容一致
- 盡量先搜尋，一般來說程式語言的大部分術語是一樣的，可以參考[這個網站](http://jjhou.boolan.com/terms.htm)
- 如果以上兩條都沒有找到合適的結果，請自己決定一個合適的翻譯或者直接使用英文原文，後期校對的時候會進行統一
- 校稿時，若有發現沒有被翻譯成台灣術語的大陸術語，可以將它新增到 translation.json 中
- 可以主動提交替換過的文本給我，或是僅提交新增過的 translation.json 也可，我會再進行文本的替換
- 請務必確定提交的翻譯對照組不會造成字串循環替代（ex: 因為「類」->「類別」，造成下次再執行自動翻譯時「類別」又變成「類別別」）

對翻譯有任何意見都歡迎發 issue，我看到了會盡快回覆

## 參加步驟

參考 [Swift 說明](https://github.com/tommy60703/the-swift-programming-language-in-traditional-chinese/)，欲翻譯章節就直接在 github 上發 Issue 中註明或直接發Pull Request 修改。m(_ _)m
有些朋友可能不太清楚如何幫忙翻譯，我這裡寫一個簡單的流程，大家可以參考一下：

1. 首先 fork 我的項目
2. 把 fork 過去的項目也就是你的項目 clone 到你的本地
3. 在命令行執行 `git branch develop` 來建立一個新分支
4. 執行 `git checkout develop` 來切換到新分支
5. 執行 `git remote add upstream https://github.com/philipz/docker_practice` 把我的庫新增為遠端庫
6. 執行 `git remote update`更新
7. 執行 `git fetch upstream master` 拉取我的庫的更新到本地
8. 執行 `git rebase upstream/master` 將我的更新合並到你的分支

這是一個初始化流程，只需要做一遍就行，之後請一直在 develop 分支進行修改。

如果修改過程中我的庫有了更新，請重復 6、7、8 步。

修改之後，首先 push 到你的庫，然後登錄 GitHub，在你的 repo 的首頁可以看到一個 `pull request` 按鈕，點擊它，填寫一些說明資訊，然後提交即可。

## 原出處及參考資料
1. [Docker —— 从入门到实践](https://github.com/yeasy/docker_practice/)
2. [《The Swift Programming Language­》正體中文版](https://github.com/tommy60703/the-swift-programming-language-in-traditional-chinese/)
