# 简介

[Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat)的分支。使用 GitHub Actions 北京时间每天早上 6 点自动构建，保证规则最新。


### geoip.dat

- 通过仓库 [@Loyalsoldier/geoip](https://github.com/Loyalsoldier/geoip) 生成
- 默认使用 [MaxMind GeoLite2 Country CSV 数据](https://github.com/Loyalsoldier/geoip/blob/release/GeoLite2-Country-CSV.zip)生成各个国家和地区的 GeoIP 文件。所有可供使用的国家和地区 geoip 类别（如 `geoip:cn`，两位英文字母表示国家或地区），请查看：[https://www.iban.com/country-codes](https://www.iban.com/country-codes)
- 中国大陆 (`geoip:cn`) IPv4 地址数据融合了 [IPIP.net](https://github.com/17mon/china_ip_list/blob/master/china_ip_list.txt) 和 [@gaoyifan/china-operator-ip](https://github.com/gaoyifan/china-operator-ip/blob/ip-lists/china.txt)
- 中国大陆 (`geoip:cn`) IPv6 地址数据融合了 MaxMind GeoLite2 和 [@gaoyifan/china-operator-ip](https://github.com/gaoyifan/china-operator-ip/blob/ip-lists/china6.txt)
- 新增类别（方便有特殊需求的用户使用）：
  - `geoip:cloudflare`
  - `geoip:cloudfront`
  - `geoip:facebook`
  - `geoip:fastly`
  - `geoip:google`
  - `geoip:netflix`
  - `geoip:telegram`
  - `geoip:twitter`

> 希望定制 `geoip.dat` 文件？需要适用于其他代理软件的 GeoIP 格式文件？查看项目 [@Loyalsoldier/geoip](https://github.com/Loyalsoldier/geoip)。

### geosite.dat

- 基于 [@v2fly/domain-list-community/data](https://github.com/v2fly/domain-list-community/tree/master/data) 数据，通过仓库 [@Loyalsoldier/domain-list-custom](https://github.com/Loyalsoldier/domain-list-custom) 生成
- **加入大量中国大陆域名、Apple 域名和 Google 域名**：
  - [@felixonmars/dnsmasq-china-list/accelerated-domains.china.conf](https://github.com/felixonmars/dnsmasq-china-list/blob/master/accelerated-domains.china.conf) 加入到 `geosite:china-list` 和 `geosite:cn` 类别中
  - [@felixonmars/dnsmasq-china-list/apple.china.conf](https://github.com/felixonmars/dnsmasq-china-list/blob/master/apple.china.conf) 加入到 `geosite:geolocation-!cn` 类别中（如希望本文件中的 Apple 域名直连，请参考下面 [geosite 的 Routing 配置方式](https://github.com/elysias123/v2ray-rules-dat#geositedat-1)）
  - [@felixonmars/dnsmasq-china-list/google.china.conf](https://github.com/felixonmars/dnsmasq-china-list/blob/master/google.china.conf) 加入到 `geosite:geolocation-!cn` 类别中（如希望本文件中的 Google 域名直连，请参考下面 [geosite 的 Routing 配置方式](https://github.com/elysias123/v2ray-rules-dat#geositedat-1)）
- **加入 GFWList 域名**：
  - 基于 [@gfwlist/gfwlist](https://github.com/gfwlist/gfwlist) 数据，通过仓库 [@cokebar/gfwlist2dnsmasq](https://github.com/cokebar/gfwlist2dnsmasq) 生成
  - 加入到 `geosite:gfw` 类别中，供习惯于 PAC 模式并希望使用 [GFWList](https://github.com/gfwlist/gfwlist) 的用户使用
  - 同时加入到 `geosite:geolocation-!cn` 类别中
- **加入 AWAvenue-Ads-Rule 广告域名**：通过 [@TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) 获取并加入到 `geosite:category-ads-all` 和 `geosite:category-ads-AWAvenueAdsRule` 类别中（口径为广告+隐私，剔除 unwelcome 功能域名）
- **新增 `geosite:category-ads-official` 独立分类**：将**原版官方** `category-ads-all`（即 [@v2fly/domain-list-community/data/category-ads-all](https://github.com/v2fly/domain-list-community/tree/master/data)，构建期展开 include 索引）单独抽取成一个命名分类。它是大合集 `geosite:category-ads-all` 的一个**子集**，适合只想用官方原版广告规则、不要额外新源的用户。
- **`geosite:category-ads-all` 大合集 = `category-ads-official` ∪ `category-ads-AWAvenueAdsRule`**：广告规则仅保留官方 + AWAvenue 两个来源，其余 EasyList / AdGuard DNS Filter / Peter Lowe / Dan Pollock 等激进全量源一律移除（2026-09-02 用户拍板，避免误杀正常功能）。
- **加入 Windows 操作系统相关的系统升级和隐私跟踪域名**：
  - 基于 [@crazy-max/WindowsSpyBlocker](https://github.com/crazy-max/WindowsSpyBlocker/tree/master/data/hosts) 数据
  - [**慎用**] Windows 操作系统使用的隐私跟踪域名 [@crazy-max/WindowsSpyBlocker/hosts/spy.txt](https://github.com/crazy-max/WindowsSpyBlocker/blob/master/data/hosts/spy.txt) 加入到 `geosite:win-spy` 类别中
  - [**慎用**] Windows 操作系统使用的系统升级域名 [@crazy-max/WindowsSpyBlocker/hosts/update.txt](https://github.com/crazy-max/WindowsSpyBlocker/blob/master/data/hosts/update.txt) 加入到 `geosite:win-update` 类别中
  - [**慎用**] Windows 操作系统附加的隐私跟踪域名 [@crazy-max/WindowsSpyBlocker/hosts/extra.txt](https://github.com/crazy-max/WindowsSpyBlocker/blob/master/data/hosts/extra.txt) 加入到 `geosite:win-extra` 类别中
  - 关于这三个类别的使用方式，请参考下面 [geosite 的 Routing 配置方式](https://github.com/elysias123/v2ray-rules-dat#geositedat-1)
- **可添加自定义直连和代理域名**：由于上游域名列表更新缓慢或缺失某些域名，所以引入**需要添加的域名**列表。[`hidden 分支`](https://github.com/elysias123/v2ray-rules-dat/tree/hidden)里的 `direct.txt`、`proxy.txt` 分别存放自定义的需要添加的直连、代理域名，最终分别加入到 `geosite:cn`、`geosite:geolocation-!cn` 类别中（`reject.txt` 自定义广告通道已随 2026-09-02 广告源精简一并移除，如需可再加回）
- **可移除自定义直连和代理域名**：由于上游域名列表存在需要被移除的域名，所以引入**需要移除的域名**列表。[`hidden 分支`](https://github.com/elysias123/v2ray-rules-dat/tree/hidden)里的 `direct-need-to-remove.txt`、`proxy-need-to-remove.txt` 分别存放自定义的需要从 `direct-list`（直连域名列表）、`proxy-list`（代理域名列表）移除的域名

### 广告分类（`category-ads-*`）是如何加工的

广告规则仅保留**两个来源**，经统一流水线生成三个分类。每次构建后，Release 正文会附上当前各分类的条数统计。

**加工流水线（官方源快照 → AWAvenueAdsRule 自转 → 并集去重）**

1. **官方源快照为 `category-ads-official`**：构建一开始，先把 v2fly 官方 `data/category-ads-all`（35 行 `include` 指令的索引文件）原样 `cp` 成独立分类。构建器在编译期将其**展开**为 v2fly 官方全量（911 条：748 domain + 162 full，与 v2fly 官方发布版 dlc.dat 逐条一致）。
2. **AWAvenueAdsRule 子集自转为 `category-ads-AWAvenueAdsRule`**：从 [AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) 的 `build/rule/` 源文件（domain / privacy / suffix / keyword）拉取后自行清洗转换，**不再直接复用官方 Geosite**：
   - `domain` + `privacy` + `suffix` 三类行合并，剥壳为裸域名（等价 AdGuard `\|\|domain^` 的后缀匹配语义）；
   - `keyword` 行加 `keyword:` 前缀补回（官方 Geosite 构建会丢弃 keyword 行，故手动补 5 条）；
   - `ip`/`ip6`/`regex` 等 geosite 格式不支持的行，与官方行为一致正常丢弃。
3. **并集生成 `category-ads-all`**：`category-ads-official` ∪ `category-ads-AWAvenueAdsRule` 后 `sort -u` 去重即得大合集。最终条数**不是**两者简单相加——重叠域名会被 trie 父域覆盖吸收（对后缀匹配语义无损）。

**遵循的原则（宁少拦，不误伤）**

- **只用官方 + AWAvenueAdsRule 两源**：EasyList（52k）/ AdGuard DNS Filter（178k）/ Peter Lowe / Dan Pollock 等激进全量源一律不引入。它们会把正常功能域名（下载站、CDN、统计前缀等）整段误拦，拦错代价远高于漏拦。
- **AWAvenueAdsRule 口径 = 广告 + 隐私，剔除 `unwelcome`**：只取 `rule/`（广告）+ `privacy/`（隐私跟踪）两个子目录，**不取** `unwelcome/` 下的 P2P/推送/升级/HTTPDNS/STUN 等功能性域名，避免把正常功能域名当广告杀掉。与官方 `Filters/AWAvenue-Ads-Rule-Adguard-No.Unwelcome.txt` 逐条等价。
- **裸域名后缀语义（含子域）**：AWAvenueAdsRule 子集输出裸域名（非 `full:`），dae / v2ray 等按**后缀匹配**，等价 AdGuard 的 `\|\|domain^`（该域及全部子域），与 9/1 前的 `full:` 前缀相比不漏子域。
- **`full:` 仅官方保留**：官方源里的 162 条 `full:` 精确域名原样保留（它们是官方口径，本就该精确匹配）。
- **keyword 保底**：AWAvenueAdsRule 的 keyword 规则补回而非丢弃——有些广告不以独立域名出现（如 URL 特征），keyword 是唯一拦截手段。

## 下载地址

> 如果无法访问域名 `raw.githubusercontent.com`，可以使用第二个地址 `cdn.jsdelivr.net`。
> 如果无法访问域名 `cdn.jsdelivr.net`，可以将其替换为 `fastly.jsdelivr.net`。
>
> *.sha256sum 为校验文件。

- **geoip.dat**：
  - [https://github.com/itoywh/geosite-ads/releases/latest/download/geoip.dat](https://github.com/itoywh/geosite-ads/releases/latest/download/geoip.dat)
  - [https://cdn.jsdelivr.net/gh/itoywh/geosite-ads@release/geoip.dat](https://cdn.jsdelivr.net/gh/itoywh/geosite-ads@release/geoip.dat)
- **geosite.dat**：
  - [https://github.com/itoywh/geosite-ads/releases/latest/download/geosite.dat](https://github.com/itoywh/geosite-ads/releases/latest/download/geosite.dat)
  - [https://cdn.jsdelivr.net/gh/itoywh/geosite-ads@release/geosite.dat](https://cdn.jsdelivr.net/gh/itoywh/geosite-ads@release/geosite.dat)

## 使用方式

**见[@Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat)**

## 致谢

- [@Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat)
- [@Loyalsoldier/geoip](https://github.com/Loyalsoldier/geoip)
- [@v2fly/domain-list-community](https://github.com/v2fly/domain-list-community)
- [@Loyalsoldier/domain-list-custom](https://github.com/Loyalsoldier/domain-list-custom)
- [@felixonmars/dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list)
- [@gfwlist/gfwlist](https://github.com/gfwlist/gfwlist)
- [@cokebar/gfwlist2dnsmasq](https://github.com/cokebar/gfwlist2dnsmasq)
- [@TG-Twilight/AWAvenue-Ads-Rule](https://github.com/TG-Twilight/AWAvenue-Ads-Rule)
- [@crazy-max/WindowsSpyBlocker](https://github.com/crazy-max/WindowsSpyBlocker)
