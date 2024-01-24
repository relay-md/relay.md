# Changelog

<!--next-version-placeholder-->

## v1.6.2 (2024-01-24)
### Fix
* Typo ([`9b2e3fc`](https://github.com/knowledgemd/backend/commit/9b2e3fcf12d76b0e7fa958002eeae4cd5661c676))
* Sitemap for googlebot ([`a3a83a0`](https://github.com/knowledgemd/backend/commit/a3a83a05b44ab472576bd5be1ceb78611a1b00e4))
* Recurrring payments typo ([`3839c7d`](https://github.com/knowledgemd/backend/commit/3839c7d2bd48c5bee89d0d34d2d015755a2b2339))

## v1.6.1 (2024-01-22)
### Fix
* Need to obtain email for github through additional request ([`88bbec4`](https://github.com/knowledgemd/backend/commit/88bbec407ba82a739a9e6206faa6cb481d5bec54))
* Unittests ([`8e05a86`](https://github.com/knowledgemd/backend/commit/8e05a86fe45b63171e9f450c3c569420e57e2ae6))

## v1.6.0 (2024-01-22)
### Feature
* **marketing:** Video demonstrating how it works ([`183a3f2`](https://github.com/knowledgemd/backend/commit/183a3f277a5f56d950f13c85b16f715550fd6dd1))

### Fix
* Unittests no longer can test x-relay-* attributes ([`9e511a6`](https://github.com/knowledgemd/backend/commit/9e511a656cb991465a566599e08663b519655f3f))
* **billing:** An additional activation path fr the subscriptin ([`c991f5a`](https://github.com/knowledgemd/backend/commit/c991f5a48359db986eb40c771d1ede2b699e1e2b))

## v1.5.0 (2024-01-20)
### Feature
* **rate-limits:** Implement rate limits ([`498e06d`](https://github.com/knowledgemd/backend/commit/498e06d09e26949e6f4458a8d382e44574a733a2))
* **prerender:** Make use of prerender to show documents ([`2e59a8d`](https://github.com/knowledgemd/backend/commit/2e59a8d3a6954e896520e0bab800488cc03cd159))
* List news sites in sitemap ([`d8a18fe`](https://github.com/knowledgemd/backend/commit/d8a18fed34bf7c754cde029a5dff3b2afd93675c))

### Fix
* Set initial datetime for access token to 2020 ([`d47570f`](https://github.com/knowledgemd/backend/commit/d47570fb4c0fe4a880fed938cdc54c842d79b9da))

## v1.4.1 (2024-01-18)
### Fix
* **billing:** An additional activation path fr the subscriptin ([`5f3c2ee`](https://github.com/knowledgemd/backend/commit/5f3c2ee42c8318cedaff472397e9d408f3b35fa8))

## v1.4.0 (2024-01-15)
### Feature
* Separate onboarding stage to have tos/privacy confirmed ([`dee3010`](https://github.com/knowledgemd/backend/commit/dee30107a6f57e88045c6234747fa04d5370d881))
* **pricing:** Any change to public perms requires payment ([`fa2dd53`](https://github.com/knowledgemd/backend/commit/fa2dd5377965c544a02f9ae137f1f5a145e10a26))

### Fix
* Set initial datetime for access token to 2020 ([`73a95eb`](https://github.com/knowledgemd/backend/commit/73a95eb24b3f9c9f265d612f8c2381f80922e165))

## v1.3.2 (2024-01-14)
### Fix
* Layout.pug had wrong intendation and missing tag ([`2f47ce8`](https://github.com/knowledgemd/backend/commit/2f47ce8911b254363927f6633c271d3cfb49bddb))

## v1.3.1 (2024-01-11)
### Fix
* Js functions were unavailable in browser ([`bc06e46`](https://github.com/knowledgemd/backend/commit/bc06e460903234d31c80b6a1c703ec54501a57ea))

## v1.3.0 (2024-01-11)
### Feature
* **htmx:** Searchable topics ([`be0f8b3`](https://github.com/knowledgemd/backend/commit/be0f8b30c5570a8097f44a47d0d09da702c85da5))

### Fix
* Sitemap.xml format was not accepted by google due to datetime and missing namespace ([`d4a0715`](https://github.com/knowledgemd/backend/commit/d4a0715012c1780bc29798fcd7bfbd387520f385))
* Typo ([`6455051`](https://github.com/knowledgemd/backend/commit/6455051e1678ef81a429b9cb65a46dcf4a17158b))

## v1.2.1 (2024-01-07)
### Fix
* More meta details in layout ([`597096e`](https://github.com/knowledgemd/backend/commit/597096e3a4fa85520954c6023486e874292716a5))
* Target: _blank with noopener ([`c8bf0d3`](https://github.com/knowledgemd/backend/commit/c8bf0d37d3712ae8043170f70a669fd6e865afa2))

## v1.2.0 (2024-01-05)
### Feature
* **sitemap:** Initial implementation of sitemap ([`76993b9`](https://github.com/knowledgemd/backend/commit/76993b9f0d2d506b5e8897625e3615660a873f72))
* **esbuild+sass:** Make better use of web tools instead of loading external assets ([`94ba669`](https://github.com/knowledgemd/backend/commit/94ba6691c20389deb790929f2f175885a4075fd9))

### Fix
* Team hide is a premium feature, really ([`9f1adec`](https://github.com/knowledgemd/backend/commit/9f1adec74382b5f0dbfada9f898ff1157635296e))
* Ensure we have the required files handy, even if empty (requires build with esbuild) ([`e2e5edf`](https://github.com/knowledgemd/backend/commit/e2e5edfedc4f84a03bfd1bac22953003ddd95a1f))
* **seo:** Make requested changes to layout ([`9be9639`](https://github.com/knowledgemd/backend/commit/9be9639781a89480bb34f0109034faf6b1baf9e4))

## v1.1.0 (2024-01-02)
### Feature
* **matomo:** Add tracking code ([`fa11c00`](https://github.com/knowledgemd/backend/commit/fa11c001c6bbde6f17beb059ca812391cc65b555))

### Fix
* Remove early access terms ([`593ae5b`](https://github.com/knowledgemd/backend/commit/593ae5b9e1ba919b6d2f58c3082fc96b3733cdde))

## v1.0.1 (2023-12-31)
### Fix
* Public documents do not require checks to read ([`d8173f9`](https://github.com/knowledgemd/backend/commit/d8173f947d9af9d64c8da6b9c853a5b26e632822))

## v1.0.0 (2023-12-31)
### Feature
* **early-access:** End of closed beta, go public ([`e9e8fa2`](https://github.com/knowledgemd/backend/commit/e9e8fa22d25422313cfe9406b879d6ed52a8bf9b))

### Breaking
* end of closed beta  ([`e9e8fa2`](https://github.com/knowledgemd/backend/commit/e9e8fa22d25422313cfe9406b879d6ed52a8bf9b))

## v0.18.0 (2023-12-30)
### Feature
* **teams:** Selected teams, search for teams ([`c458f7f`](https://github.com/knowledgemd/backend/commit/c458f7f423702e5ab4bf2243dc1c1d57cba77303))

### Fix
* Team list with headline looks better now ([`fbaff14`](https://github.com/knowledgemd/backend/commit/fbaff14b3facccec4eaabf1fbc6c011119bd7772))
* Make sentry optional ([`c36799b`](https://github.com/knowledgemd/backend/commit/c36799be4d3f4942c2c236716e6cb8673a6687f1))

## v0.17.1 (2023-12-29)
### Fix
* Tests ([`babba50`](https://github.com/knowledgemd/backend/commit/babba5059c4830dfc9c141ee87e4679a65b435e9))
* Require a github username for oauth ([`4986a17`](https://github.com/knowledgemd/backend/commit/4986a178bd131ec585a88880bdf9a23216a82197))
* Additional test for empty upload ([`4d4b289`](https://github.com/knowledgemd/backend/commit/4d4b289e7b5363ca824de3ea81e9523c051f4101))
* Linting ([`52b3513`](https://github.com/knowledgemd/backend/commit/52b35135c16548e9f7c28642f477b844632e98e7))

## v0.17.0 (2023-12-27)
### Feature
* **subscription:** Deal with subscriptions using stripe webhooks ([`c0f0ae5`](https://github.com/knowledgemd/backend/commit/c0f0ae55e00d52e9e214fa75cb4416cc650cb128))

### Fix
* Unittests ([`c7e6334`](https://github.com/knowledgemd/backend/commit/c7e633430d32e7f3b63a7d2b9314dee4b850ab62))

## v0.16.5 (2023-12-25)
### Fix
* Obtain emails thru api in case profile has no default email ([`4078ed7`](https://github.com/knowledgemd/backend/commit/4078ed76960a63bddeb71be4c26daa9285e04b08))

## v0.16.4 (2023-12-23)
### Fix
* Only activate a subscription if it gets paid ([`eb7a55e`](https://github.com/knowledgemd/backend/commit/eb7a55e4500ed82e58d9a2e7cfcea09bcdb49141))
* Default seats=1 ([`d9a3285`](https://github.com/knowledgemd/backend/commit/d9a3285d95c128c9ba4677ec889856977566afcc))

## v0.16.3 (2023-12-23)
### Fix
* **stripe:** Submit the customer id in the session ([`c4f0cfd`](https://github.com/knowledgemd/backend/commit/c4f0cfd9185cdfc9e7cce530f300bae58d15b68c))

## v0.16.2 (2023-12-23)
### Fix
* **stripe:** Proration_behavior invalid here ([`a02c73f`](https://github.com/knowledgemd/backend/commit/a02c73f6acd175923803ce012774a3eede184f41))

## v0.16.1 (2023-12-23)
### Fix
* Obtain access_token from doc, linting ([`078ec6c`](https://github.com/knowledgemd/backend/commit/078ec6c5c365644798ad237f7b18e145767ea4a0))
* Typo ([`de7840f`](https://github.com/knowledgemd/backend/commit/de7840fdedbc8d0bfb3b857d7748f9c09fa0bfad))
* Typo ([`16c7df6`](https://github.com/knowledgemd/backend/commit/16c7df68206ea9b232ca72e4e4d9fb27da2b064f))

## v0.16.0 (2023-12-22)
### Feature
* **seats:** Implement seats for subscription ([`7a3e53a`](https://github.com/knowledgemd/backend/commit/7a3e53aa08da311c6cb623cb2f67e14a500f5f5d))

### Fix
* Unittests ([`9c1bbf8`](https://github.com/knowledgemd/backend/commit/9c1bbf8442ca94aeceecc2233dd04090b09be518))
* **billing:** Properly deal with subscription periods ([`9b50715`](https://github.com/knowledgemd/backend/commit/9b507156aff61556beb80387f5b8f05d72818235))

## v0.15.0 (2023-12-22)
### Feature
* **contact form:** Add a contact form ([`5af5d80`](https://github.com/knowledgemd/backend/commit/5af5d80b29f352e82ed370f7c85cbd568d6e3ce5))
* **perms:** Require read/post for unpaid teams ([`9df1e53`](https://github.com/knowledgemd/backend/commit/9df1e53773935cd2589dd85771f8be46ecd47c50))
* **team:** Allow to hide a team ([`8838468`](https://github.com/knowledgemd/backend/commit/8838468c7edba92dd4caf3024562d8a693b52ed3))
* **pug:** Consistently use pug over html templates ([`d63086a`](https://github.com/knowledgemd/backend/commit/d63086a68c9be2150735aef530e6067c728e8c41))
* **stripe:** Offload stripe specifics into separate tables ([`ef14b58`](https://github.com/knowledgemd/backend/commit/ef14b5854bbd55405955df465d02a696f99153d3))
* Sort teams by members ([`48eb0d8`](https://github.com/knowledgemd/backend/commit/48eb0d8e26255fe034035887f5d5b96be095d5d6))
* **susbcriptions:** Run the numbers by users per team ([`3f80d3d`](https://github.com/knowledgemd/backend/commit/3f80d3dee647ca0823d636f78d0d9fec0902a2cd))

### Fix
* Proper subscription handling with price ([`3d4520d`](https://github.com/knowledgemd/backend/commit/3d4520d2cc53fd4839bfc8f3fd4e774364a6815f))
* Permissions and list of teams with no members ([`bd72164`](https://github.com/knowledgemd/backend/commit/bd72164c1d83a6cee7acd67708e1341f090e9613))
* Unittests ([`a14eed1`](https://github.com/knowledgemd/backend/commit/a14eed1c52627e92165ab660ccf7ec2fe2445d38))
* Proper redirect ([`95de82d`](https://github.com/knowledgemd/backend/commit/95de82dfe4f67875000c4f6bd7868f07606bb40b))
* Database must do pre_ping by default ([`902a11a`](https://github.com/knowledgemd/backend/commit/902a11a1f0b1e9718749e30ad7bdcac52c985a50))
* Proper payment return URLs ([`19952b9`](https://github.com/knowledgemd/backend/commit/19952b9f36e731d1cf74ce93a448dc8681a544db))
* Cyclic import error resovled ([`9ef3017`](https://github.com/knowledgemd/backend/commit/9ef3017b77e381e0a45b022a8ceece91ecfaf8e9))
* Unittests ([`712d1d1`](https://github.com/knowledgemd/backend/commit/712d1d14abaf747fc4802decd788c3a82e45130c))
* Add HMAC and favicon ([`78ddf78`](https://github.com/knowledgemd/backend/commit/78ddf7819ea4b70bd5f75f3c78491f9acd349df0))
* **tos:** More text ([`74b9fd7`](https://github.com/knowledgemd/backend/commit/74b9fd7743bfe29e97ded938f30e6a3b0f55e19f))

## v0.14.1 (2023-12-15)
### Fix
* Email validation ([`773082e`](https://github.com/knowledgemd/backend/commit/773082e8feb0f7458c56d6fd269f235ccfe206bd))

## v0.14.0 (2023-12-10)
### Feature
* **news:** Nicer news page ([`cfd71dd`](https://github.com/knowledgemd/backend/commit/cfd71ddadf96fc94c1efeecb8795daf5faf96c4f))
* **news:** Initial work on news site ([`a2ca506`](https://github.com/knowledgemd/backend/commit/a2ca506dde8a34ecf87fc89d50524a86a0ea1489))

### Fix
* **requirements:** Downgrade mysqlclient to make docker build again ([`4dec830`](https://github.com/knowledgemd/backend/commit/4dec830bd9376ef21060f6c1fc232967c3a6ee7c))
* Add var to tests ([`8238c00`](https://github.com/knowledgemd/backend/commit/8238c004a33e0eb0ee9670d48305eb4251720504))

## v0.13.1 (2023-12-10)
### Fix
* **requirements:** Pin mysqlclient so it build in docker ([`df97a5b`](https://github.com/knowledgemd/backend/commit/df97a5bd42dfd32a2624120b63161e8928219da8))

## v0.13.0 (2023-12-10)
### Feature
* Allow to use markdown in pug ([`9d186f0`](https://github.com/knowledgemd/backend/commit/9d186f028f1e5eb1a78a0f05c03c2b0d34f9bc0e))
* Allow to select oauth provider (google, github) ([`9033933`](https://github.com/knowledgemd/backend/commit/9033933d3f76d3b9e8a5f0c4d669e22c0248a38c))
* Show oauth provider when listing users ([`692318c`](https://github.com/knowledgemd/backend/commit/692318c6538c0f058892b30afaa1ce063dfdd9d5))
* Force google users to provide a username ([`777181f`](https://github.com/knowledgemd/backend/commit/777181f20bbd3b350f44b1190af35b2ba9e7f4a6))
* Oauth via google ([`0d36526`](https://github.com/knowledgemd/backend/commit/0d36526df32293310e3476e3f70e8e6f2672a2fc))
* **pydantic-v2:** Migration to pydantic v2 ([`3f729b1`](https://github.com/knowledgemd/backend/commit/3f729b108f4eeebd868c30907ecd8ce57ec76a73))
* List of members in a team ([`4c1a1db`](https://github.com/knowledgemd/backend/commit/4c1a1db14db03962c06e29af9095b48e07fabd12))
* Invite users to a team ([`e49bd1c`](https://github.com/knowledgemd/backend/commit/e49bd1c162c47622ec50ab8e0ed326588af46fa2))
* Allow to post documents for members ([`4c525cf`](https://github.com/knowledgemd/backend/commit/4c525cfd85974865a4ae523e3ad860a19cde9a62))
* Explanation for relay-title ([`61d16da`](https://github.com/knowledgemd/backend/commit/61d16da990eb820ea054e23ab6f111ce8e5e2889))
* **pagination:** Paginate on separate documents page ([`523f559`](https://github.com/knowledgemd/backend/commit/523f559c33b13d91f0bf20b77e67702af22020ec))

### Fix
* Remove google login for now ([`6cf732f`](https://github.com/knowledgemd/backend/commit/6cf732fb8f6b6c3a1b8cab3b024b8fcf0ddebee0))
* Add tos to footer ([`93e5174`](https://github.com/knowledgemd/backend/commit/93e5174b35156bd8a93e707a635110e1af1d38bf))
* Tests ([`493e450`](https://github.com/knowledgemd/backend/commit/493e450b99180ff23ba6345285904bfb1aacbe74))
* Typo ([`d013184`](https://github.com/knowledgemd/backend/commit/d013184f2813eaf9250d86c88b66b42274b29c64))
* Unique constraints on Indices ([`27752bf`](https://github.com/knowledgemd/backend/commit/27752bf69dd7443d40afaa7c0f06c49c6f27ad31))

## v0.12.0 (2023-12-07)
### Feature
* Explanation for relay-title ([`4db3ad0`](https://github.com/knowledgemd/backend/commit/4db3ad05cdc62d803b6376729f78510647e69873))
* **join:** Allow a user to join a team, prevent posting to restricted or private teams ([`8975fd2`](https://github.com/knowledgemd/backend/commit/8975fd26d122aed3766d1f029f08392f50113ab1))
* **team-membership:** Enable to be part of a team, indpendent of subscriptions ([`ce89522`](https://github.com/knowledgemd/backend/commit/ce89522d61f78c879e3cce2396c1c35af03a91b1))
* More flexible team.type ([`1cfd902`](https://github.com/knowledgemd/backend/commit/1cfd90286f534b36c36040ecf935b145a10ac790))

### Fix
* Flip icons for dark/light mode ([`1fc2209`](https://github.com/knowledgemd/backend/commit/1fc2209dcd8f5eae7a6d03545510791127d40320))

## v0.11.0 (2023-12-06)
### Feature
* Automatically subscribe to news@relay.md ([`4983140`](https://github.com/knowledgemd/backend/commit/4983140d24daad46f82d103fea380211afe81acb))
* **web:** Dark/light switcher ([`2dc7269`](https://github.com/knowledgemd/backend/commit/2dc72699085bc781498d0ec92a9fa91d188475ff))
* Store documents in subfolders on minio ([`83c4f45`](https://github.com/knowledgemd/backend/commit/83c4f45661776163c712a447e90ea7f02ce1cb42))
* **title:** Store document title in database ([`efad9a8`](https://github.com/knowledgemd/backend/commit/efad9a86b97f9fd61232571156ae911cb6906e79))

### Fix
* Typing error in py38 ([`e657a77`](https://github.com/knowledgemd/backend/commit/e657a7748b73d344fba3e9e911336645cb20ac3e))
* Create documents could be called with string argument ([`003aa25`](https://github.com/knowledgemd/backend/commit/003aa253cf194fb9b284102b85cc133a9865e5e7))
* Shared/owned document list in profile ([`5950bd0`](https://github.com/knowledgemd/backend/commit/5950bd0c66fcf04c1b997e8201e748266e522526))
* Wrong logic ([`469e381`](https://github.com/knowledgemd/backend/commit/469e381aa19ff267e2f5466450505e06270eee21))
* Only show teams when logged or leave early access mode ([`d767cfc`](https://github.com/knowledgemd/backend/commit/d767cfca6f96e1884ad6ef7eedff8b8038d2af19))

## v0.10.0 (2023-12-06)
### Feature
* Proper testing for subscriptions and listing of posts ([`b8aa95a`](https://github.com/knowledgemd/backend/commit/b8aa95ab710a67eae3a7f07d1727a39e30b6eaab))
* Allow to subscribe to team/topics ([`98eebe5`](https://github.com/knowledgemd/backend/commit/98eebe5181aa4a37f6c2eeb8d4e412f6c31e026d))
* **cli:** More powerfull cli tools ([`5f09225`](https://github.com/knowledgemd/backend/commit/5f09225ed0f2f6e008474abd4b8f0acf161ed2d0))

### Fix
* Update the datetime on PUT ([`993b95d`](https://github.com/knowledgemd/backend/commit/993b95d107b3fb4902c4834b4ccae8ef1332bd69))

## v0.9.0 (2023-12-02)
### Feature
* Include prometheus exporter ([`e7ba269`](https://github.com/knowledgemd/backend/commit/e7ba269201657d1943652b25c0ca8e8d727add06))

## v0.8.0 (2023-12-02)
### Feature
* **hijs:** Code highlighting in viewer ([`f855b9b`](https://github.com/knowledgemd/backend/commit/f855b9b6463b301d93623bc433bc3b9d301df6eb))
* Allow to read public docs without api-key ([`0d721ef`](https://github.com/knowledgemd/backend/commit/0d721ef28b257b55c15c7d637e0a4b277b103433))

## v0.7.0 (2023-12-02)
### Feature
* Deal with redirects during auth/login/register etc ([`96f2aa1`](https://github.com/knowledgemd/backend/commit/96f2aa13ad7d564e1606c899367ef3f1f0b7733d))
* Allow to configure obsidian with a single click ([`9d1f15f`](https://github.com/knowledgemd/backend/commit/9d1f15fd2ca48bde05fa98f9c5c831a113f294eb))
* Explain attributes, list teams ([`d7caa2b`](https://github.com/knowledgemd/backend/commit/d7caa2be4a165f9b812f390a9a6b54446f3eeba3))

### Fix
* Give frontmatter filename priority over query string ([`cb9b734`](https://github.com/knowledgemd/backend/commit/cb9b734320cc7af26b73f046e40d3f0553fb5c5b))

## v0.6.1 (2023-12-01)
### Fix
* Unittests need to compliy with new status codes ([`3c49ec8`](https://github.com/knowledgemd/backend/commit/3c49ec880b19afd41024c20ff5fe6aaf589ced1e))
* Improve error handling ([`1c6e73b`](https://github.com/knowledgemd/backend/commit/1c6e73bd692bf6421e99c620c47711125c690f8a))

## v0.6.0 (2023-12-01)
### Feature
* Public docs and read-password ([`2d6c4c8`](https://github.com/knowledgemd/backend/commit/2d6c4c836742e2d4035521c59b24b8165e7ac2f3))
* **web:** A site that explains how to install the plugin ([`4b0c2ba`](https://github.com/knowledgemd/backend/commit/4b0c2ba137a1d53cacae0ede97fd242bf3406651))

### Fix
* Reuse team.is_private instead of hardcoding _ ([`3c56020`](https://github.com/knowledgemd/backend/commit/3c56020d5c5e769f89b6b18aebfaee2fff9b636c))

## v0.5.0 (2023-11-30)
### Feature
* How it works ([`509efec`](https://github.com/knowledgemd/backend/commit/509efeccaf49dda5c2744fd7c616468a0a5ec011))
* Allow sharing docs with users ([`31c6711`](https://github.com/knowledgemd/backend/commit/31c6711ca507f62ed3d63e3d4c959345136e165e))
* Initial work on permission scheme ([`aec0022`](https://github.com/knowledgemd/backend/commit/aec002201e734741c39c8e0078b587a9e0ad2141))

### Fix
* Log access to documents ([`dca3115`](https://github.com/knowledgemd/backend/commit/dca311553a329eaf554f0869be8dc23552b3937e))
* Remove how it works from navbar ([`95fd349`](https://github.com/knowledgemd/backend/commit/95fd3497cae6f78de4b628e873cea9506454da4d))
* Relay_to is now called relay-to ([`55ea950`](https://github.com/knowledgemd/backend/commit/55ea950904fe4c10c740aa9ceaf39c60d0a1e19b))
* Viewer obtain documents from public api ([`1a25854`](https://github.com/knowledgemd/backend/commit/1a2585406a2ba20a56d9e9e0a6a42b1d45789e43))
* When properly logged in, show profile link ([`94688be`](https://github.com/knowledgemd/backend/commit/94688bec6b6ea7883cb059e4f67e6f21ea7871ae))
* Need config for navbar ([`4e30b5b`](https://github.com/knowledgemd/backend/commit/4e30b5b355b4867dbdf4dbdf59fff72e1c6de5c6))

## v0.4.1 (2023-11-30)
### Fix
* Forcing release ([`761d5be`](https://github.com/knowledgemd/backend/commit/761d5be65e69d9deb5d8dd4cb5982aa27f6f4d43))

## v0.4.0 (2023-11-30)
### Feature
* **put:** Allow to put an entire object ([`f6414ea`](https://github.com/knowledgemd/backend/commit/f6414ea87ba665b48d2a24c359de0cacb569036c))

### Fix
* Linting ([`c6151db`](https://github.com/knowledgemd/backend/commit/c6151dbd379481b5165e95fc968b850ec195d3d7))
* Properly patch minio ([`3fa8392`](https://github.com/knowledgemd/backend/commit/3fa839285cc8c7e89b05e591436d905a4737d799))
* Unittests now with relay-document ([`3d2bcd7`](https://github.com/knowledgemd/backend/commit/3d2bcd7a25d41bdf3426f88be0e84faf8e49cfc5))
* Remove pricing section ([`77dfa85`](https://github.com/knowledgemd/backend/commit/77dfa8516d5f8ceff0807299d11b7bf4a2f07336))
* More robust uploads, dd document-id ([`845e498`](https://github.com/knowledgemd/backend/commit/845e498086973f91aaaa42766778f2e181eab781))
* Import issues when running api and web ([`84f4d98`](https://github.com/knowledgemd/backend/commit/84f4d9810eed075d1857fcc0f297ab1b90044fd8))

## v0.3.1 (2023-11-29)
### Fix
* Deployment via nomad uses run instead of apply ([`99ece29`](https://github.com/knowledgemd/backend/commit/99ece296b122d9b62aad03ada3efe4a010013c51))

## v0.3.0 (2023-11-29)
### Feature
* **health:** Check endpoint on web ([`fecbd81`](https://github.com/knowledgemd/backend/commit/fecbd81d289ddcd78ffe9c5a96bf972f0edc7077))

## v0.2.0 (2023-11-29)
### Feature
* **tests:** Api tests happy path ([`6381bec`](https://github.com/knowledgemd/backend/commit/6381becc4b55dae1e0b67aa358e04b7d56bca3bc))
* **health:** Health endpoint and initial testing ([`f9ba732`](https://github.com/knowledgemd/backend/commit/f9ba73290f72328302a86542eea5a73fb3559d52))
* **profile:** Initial work for profile ([`8d73e4d`](https://github.com/knowledgemd/backend/commit/8d73e4de0dc276c4b5eb63d29c9ffa3f15df340b))
* **viewer:** Initial implementation for viewer ([`4f4542f`](https://github.com/knowledgemd/backend/commit/4f4542f28d3d940ebb86c3cc88a19f97fcf04ca6))
* **web:** Host homepage on backend as well ([`453359a`](https://github.com/knowledgemd/backend/commit/453359ae53ec563a4825b699b2bcbf09a7e4e7f1))
* Obtain recent docs, allow specify filename in frontmatter ([`1870c18`](https://github.com/knowledgemd/backend/commit/1870c185367b374b440b7aca6c59ce2872d4dfe2))
* Allow to obtain raw text/markdown payload ([`a69f9e1`](https://github.com/knowledgemd/backend/commit/a69f9e14d8b91cb5829230d17ca0092f7b0735f6))
* **minio:** Upload and get documents from minio/s3 ([`505db8c`](https://github.com/knowledgemd/backend/commit/505db8c03f0c981ca1c29323ca35ed664efff67c))
* Disable openapi url for web interface ([`c29477b`](https://github.com/knowledgemd/backend/commit/c29477b3c62b4109104dad2f6f88196a20cd17e4))
* **cli:** Modulerize cli tools ([`d6960e9`](https://github.com/knowledgemd/backend/commit/d6960e99fb67a16a2375ca80e2f0bcd4200de740))
* Distinct web module ([`cb898fa`](https://github.com/knowledgemd/backend/commit/cb898fad6b0e2995dba662dd16a6f69a5fb7ff7d))

### Fix
* Add mising file ([`efd3f78`](https://github.com/knowledgemd/backend/commit/efd3f7810b36af3a47fbba3e489af440543834f6))
* Linting ([`90b4de1`](https://github.com/knowledgemd/backend/commit/90b4de140485c19acbe04c2f66882bd824bde46b))
* Unittests should now work ([`59a960b`](https://github.com/knowledgemd/backend/commit/59a960b79091711d474fa50d62f09b176dbf2cc1))

## v0.1.2 (2023-11-13)
### Fix
* Another release triggered by drone hopefully ([`c286f8b`](https://github.com/knowledgemd/backend/commit/c286f8bf558112dca66fc46f0b0c7c634836272f))

## v0.1.1 (2023-11-13)
### Fix
* Proper pipelining with release ([`8dc69a1`](https://github.com/knowledgemd/backend/commit/8dc69a1411826dffcea9f3deb1444fa477812264))
