# MHWI EverythingShopList Manager

一键搞定 `shopList.slt` 重命名，快速切换“啥都有商店”。

《怪物猎人：世界》的商店MOD受游戏限制，单次最多只显示约255个商品。因此，大佬们通常会把海量物品拆分成多个 `shopList_01.slt`、`shopList_02.slt` 文件。原生的切换方式需要你切出游戏、打开文件夹、手动改文件名、再切回游戏，操作频繁且极易手滑改错。

通过MHWI EverythingShopList Manager管理 `facility` 目录下的 `.slt` 文件：把任意一份复制为游戏使用的 `shopList.slt`，或删除当前的 `shopList.slt`。

## 使用

### 单可执行文件.exe版本（推荐）

`dist` 目录中的 `MHWIShoplistManager.exe` 为单文件版，无需安装 Python。把 exe 放在项目根目录（`facility` 文件夹旁）后双击运行即可。

1. 将本工具放置于 `.../Monster Hunter World/nativePC/common/facility/` 文件夹旁。
2. 双击打开，程序会自动列出当前`facility` 目录下的已有的所有商店分页文件 `.slt` 。
3. 点击你想使用的页面编号，看到`[已启用]`提示即可。

### 命令行（没必要）

```text
py -3 main.py scan
py -3 main.py enable 3
py -3 main.py enable "shopList_08下位素材、矿骨、上位熔山龙.slt"
py -3 main.py disable
```

`enable` 的序号来自 `scan` 输出；`--yes` 可跳过替换或删除前的确认。

如果 `.slt` 文件不在项目根目录的 `facility` 文件夹里，可用 `--path` 指定：

```text
py -3 main.py --path "其他目录" scan
```

## 注意事项

- 建议在游戏完全关闭状态下进行切换，防止文件被占用导致修改失败。
- 首次使用前请手动备份原有的 `shopList.slt` 文件，以防万一。

## 关于《啥都有商店Mod 2》（All consumables and materials in the Shop）

> ## About this mod
>
> updated shopList for version 15.11
>
> Disclaimer
>
> I am not an actual modder, there is no point in anyone to start asking me random things etc. I only did this because I was baffled about the shopList mods not being updated for ages (such as [CaptainObnoxious](https://www.nexusmods.com/monsterhunterworld/users/25445194)'s [Sorted Shop Lists ](https://www.nexusmods.com/monsterhunterworld/mods/2005)that I personally used back then), and the only one that provided something was [apurpleliger](https://www.nexusmods.com/monsterhunterworld/users/77770448) with his updates on one [shopList](https://www.nexusmods.com/monsterhunterworld/mods/2867?tab=description) page with GL parts and new monsters' materials inserted.
> I worked based on his work with [shopList editor](https://www.nexusmods.com/monsterhunterworld/mods/507) to provide a complete package with a few improvements, like cleaning a lot of double items (when you have the whole pages package), adding materials for MR teostra/kushala/kirin/lunastra/deviljo/rajang and anything else I found missing.﻿ I also did a half-hearted lazy job on putting them KIND OF in a correct order.
> I was too lazy myself to do it for a very long time, I imagine other people are like me, so I decided to upload what I did...That's all.
> At this point I should inform you about the price range. This mod has kept to the original creator's mentality of a balance "bit" in the form of cost. Ergo, the prices are 10 times their selling value. There are ways to mess with the prices in the game, which do not interest me, so if you are interested, look it up and do it yourselves.
> Now we must NOT forget that this mod is essentially a cheat. I myself never used it to completely negate any grind I had to do in the game, but If I missed 1-2 materials for a forge/upgrade and I wouldn't get it in the next 1 or 2 hunts, I'd use it. Buuut what you guys do is your problem, AND we never know when capcom might decide that she's fed up with cheat mods and do a sweep on us for using them... warning given, I am out.
> P.S.: A quick reminder of the correct use. The path of the directory is NativePC/common/facility. The page.slt you wanna use must remain in there and be named "shopList.slt". The only thing I personally did was to create a folder inside "facility", have the pages in there and drag the one I need everytime out, into the "facility" folder, rename it to "shopList.slt" and do my job.
> P.S. 2: Oh and OF COURSE you will need [Stracker's Loader](https://www.nexusmods.com/monsterhunterworld/mods/1982?tab=description) to use this mod.
> P.S. 3: Do NOT install this mod with Vortex.

[NexusMods / All consumables and materials in the Shop](https://www.nexusmods.com/monsterhunterworld/mods/4499)

