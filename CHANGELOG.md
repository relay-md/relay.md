# CHANGELOG



## v1.19.3 (2024-05-19)

### Fix

* fix: use pat when releasing tag ([`2138c1e`](https://github.com/relay-md/relay.md/commit/2138c1e304e2ab6c2b785cc01efdca5b1f3c2874))


## v1.19.2 (2024-05-19)

### Ci

* ci: also build release docker image - try 2 ([`2c607de`](https://github.com/relay-md/relay.md/commit/2c607de657565f2e6561ca515662b02c0022b351))

### Fix

* fix: trigger new release ([`7ad6926`](https://github.com/relay-md/relay.md/commit/7ad69262ceedc2ee9ff6de77c5963cb2eec77b6b))

### Unknown

* Merge branch &#39;develop&#39; ([`b781895`](https://github.com/relay-md/relay.md/commit/b7818954cec9098b61c541b239609e98a9941c51))

* Merge pull request #4 from relay-md/release/202405191605

ci: also build release docker image - try 2 ([`afa0d62`](https://github.com/relay-md/relay.md/commit/afa0d62aad47178d01e878112822c4e9fe2cdc43))

* Merge pull request #3 from relay-md/release/202405191605

ci: also build release docker image ([`c4f0820`](https://github.com/relay-md/relay.md/commit/c4f082049a346eec554aa162be44416a008936e3))


## v1.19.1 (2024-05-19)

### Ci

* ci: also build release docker image ([`2ff71cf`](https://github.com/relay-md/relay.md/commit/2ff71cf9ebf8102a865aa3b9ed10e055eab23b36))

* ci: also build release from main ([`83f5082`](https://github.com/relay-md/relay.md/commit/83f508291081ad9793e8d2f8861ed80027209b1c))

* ci: tune drone.io config for production ([`f5c965f`](https://github.com/relay-md/relay.md/commit/f5c965f9d9ac29cd43dfec89dae8eb0f811a3703))

* ci: improve Makefile ([`5581ca1`](https://github.com/relay-md/relay.md/commit/5581ca1a74b0abee05d8f5c95f57b0cb8b23f239))

* ci: improve release procedure ([`482eccd`](https://github.com/relay-md/relay.md/commit/482eccd6550e1076cb4cc19f799eb107185fe740))

### Fix

* fix: unittests ([`7174753`](https://github.com/relay-md/relay.md/commit/7174753f1137b32bd432da97a77c54851a171141))

### Unknown

* Merge pull request #2 from relay-md/release/202405191605

ci: also build release from main ([`cad2919`](https://github.com/relay-md/relay.md/commit/cad29193e7d35df9a44fa55998b409823392301d))

* Merge pull request #1 from relay-md/release/202405191605

Release/202405191605 ([`153e4aa`](https://github.com/relay-md/relay.md/commit/153e4aab14560159c79353c74b3851e984d1d509))


## v1.19.0 (2024-05-19)

### Breaking

* feat(early-access): end of closed beta, go public

BREAKING CHANGE: end of closed beta ([`e9e8fa2`](https://github.com/relay-md/relay.md/commit/e9e8fa22d25422313cfe9406b879d6ed52a8bf9b))

### Build

* build(pre-commit): optional parameter ([`59fdc76`](https://github.com/relay-md/relay.md/commit/59fdc767395c4fa82d650f4706038dcbf523d7b3))

* build(precommit): use pre-commit on backend stuff ([`d948bf8`](https://github.com/relay-md/relay.md/commit/d948bf8a92fbeee87ab41c51a9d91d79402a5f90))

* build: proper build tools for css and js, dockerfile ([`be4b975`](https://github.com/relay-md/relay.md/commit/be4b97514d312f43d64ffa3134216d6763f28534))

* build: ignore .git repo for docker ([`9b4bd50`](https://github.com/relay-md/relay.md/commit/9b4bd505ee322c7c8ac9f90a2a84ecfaa3d917a2))

### Chore

* chore: initial db migration ([`70efa85`](https://github.com/relay-md/relay.md/commit/70efa8524bcd2523ee01d06070ccf9ec05df8f80))

* chore: bring back useful changes from relay.md ([`832c927`](https://github.com/relay-md/relay.md/commit/832c927dbabba10c3ebc82960ca62c01640d2a54))

* chore(blog): sort news by created_at ([`dc5de0e`](https://github.com/relay-md/relay.md/commit/dc5de0e59982b1c2b9d796ccc2b2df1e9fed89ae))

* chore: minor styling changes in teams list ([`c5c938a`](https://github.com/relay-md/relay.md/commit/c5c938aa144af5d895baed35d86a89d626a99e53))

* chore: move newsletter to footer ([`a6e065b`](https://github.com/relay-md/relay.md/commit/a6e065b008fe69932c87476a7d49cc0f12acb7bd))

* chore(library): infinite scroll ([`bc8f0bb`](https://github.com/relay-md/relay.md/commit/bc8f0bb369d7abf485c9f9e1636d9f521f59593c))

* chore(font): use inter primarily ([`c5e3950`](https://github.com/relay-md/relay.md/commit/c5e3950aae48c157e1b26bd01fc2054e3f1efdcb))

* chore: remove fixmes ([`6bb7e1a`](https://github.com/relay-md/relay.md/commit/6bb7e1aebc0cc080a78ab174ef5c5ca45ae6d3cf))

* chore: resolve merge conflict ([`2aa7902`](https://github.com/relay-md/relay.md/commit/2aa7902cfb17b9cdab115cd743ccb43e0e07f938))

* chore: remove irrelevant columns in invoice ([`764a13e`](https://github.com/relay-md/relay.md/commit/764a13e9fe5a1ee6fe95fe7fd8ee90c6d6022f36))

* chore(tax): let stripe deal with tax ([`78120de`](https://github.com/relay-md/relay.md/commit/78120de633ddff527c2bd3912f5477f0c85ce93e))

* chore: cleanup of unittests ([`fcf9249`](https://github.com/relay-md/relay.md/commit/fcf9249ff998d66e364c15680a0bf0c640ddfee5))

* chore: .gitignore with node modules ([`18e8eff`](https://github.com/relay-md/relay.md/commit/18e8eff725c6362ec6d44c175f8607d2a3742303))

* chore: move script to the top ([`e6c2bad`](https://github.com/relay-md/relay.md/commit/e6c2bad1b9b9a6eafe8643908f0cb2ff681d42b5))

* chore(prerender): add prerenderReady state to signal site readiness ([`91fa8b0`](https://github.com/relay-md/relay.md/commit/91fa8b0e4e181db88029b43474a59fdf2818d0b3))

* chore: make config a global parameter, remove matomo if not configured ([`dc62b6d`](https://github.com/relay-md/relay.md/commit/dc62b6d4d329bbd2c5021131b703be5016a8217c))

* chore: updates ([`63e27f8`](https://github.com/relay-md/relay.md/commit/63e27f80ec9f773d421252d39ce94d9be5c57dae))

* chore: renaming and trying to resovle prerender issues ([`e5aa3c3`](https://github.com/relay-md/relay.md/commit/e5aa3c3f2f44ac8c12da77bfbb02fb2db1483d42))

* chore: allow to reset an access token&#39;s last_document_at ([`9bee871`](https://github.com/relay-md/relay.md/commit/9bee8713fccb535d7772f8eef16a8499e4edcd4b))

* chore(assets): store filesize and checksum, return embeds for documents ([`a176dbf`](https://github.com/relay-md/relay.md/commit/a176dbfeb107c267fff0be653094ec34776f181a))

* chore: more mobile friendly ([`059bb05`](https://github.com/relay-md/relay.md/commit/059bb052baba62c219270eb389c2dc9166df0a90))

* chore: custom svg logo ([`4287fa5`](https://github.com/relay-md/relay.md/commit/4287fa5909bbaa612aa9bce8279810626bf40030))

* chore: use crown for upgraded team ([`23759ae`](https://github.com/relay-md/relay.md/commit/23759ae1d476041d11a9a2c257ecdc7a36a4a76c))

* chore: update privacy policy due to matomo ([`74060ef`](https://github.com/relay-md/relay.md/commit/74060efad9fe95cce0d453011208ab7a74e31157))

* chore: improve sitemap for google ([`3406542`](https://github.com/relay-md/relay.md/commit/3406542aca2912e5bb3b08f3103625aee22dc05b))

* chore: typo ([`531c978`](https://github.com/relay-md/relay.md/commit/531c978880235fc1171e50ece214d0924be181d6))

* chore: new description in meta ([`e336684`](https://github.com/relay-md/relay.md/commit/e336684297541dbb19ab45a3e32e65e61908e355))

* chore: provide robots.txt ([`3557d03`](https://github.com/relay-md/relay.md/commit/3557d03c01316064c2bd0dccc05cbd6e183a16d5))

* chore: add missing icons ([`4e15bf8`](https://github.com/relay-md/relay.md/commit/4e15bf84a6e1cee51e2b76bcad8a76715adc0ddf))

* chore: cleanup, fortawesome locally ([`54ce9ba`](https://github.com/relay-md/relay.md/commit/54ce9ba3b8dd489948bf957753f5f9755f288ce8))

* chore: remove static builds from git repo ([`fc9c9f5`](https://github.com/relay-md/relay.md/commit/fc9c9f59e4b5a85b79934583fb456ffe22ecae43))

* chore: configure pycodestyle ([`2668694`](https://github.com/relay-md/relay.md/commit/2668694df1acd8550b5d7826d0dfcd890a56cb0a))

* chore: deploy sentry for web and api ([`d1737c7`](https://github.com/relay-md/relay.md/commit/d1737c70ddb1a7195383c4aef4c8bcb0622fdf62))

* chore(tests): permissions tests for public permissions ([`939c8b2`](https://github.com/relay-md/relay.md/commit/939c8b23bde6512e25b0303282333e920d815557))

* chore: fix typo and add timeline template ([`e3ccc6a`](https://github.com/relay-md/relay.md/commit/e3ccc6ac9b3aa9acfe9147b63523f65c0f199577))

* chore: improve navbar and make it easier to create a team ([`d703d01`](https://github.com/relay-md/relay.md/commit/d703d018a58f210782da52589575ce14e0a75763))

* chore: improve landing page, add images to how-it-works ([`795fa7e`](https://github.com/relay-md/relay.md/commit/795fa7eb8a84b28437c8c36a9a0d7c70682ac86a))

* chore: improve presentation of api ([`d0bdd80`](https://github.com/relay-md/relay.md/commit/d0bdd80a958457e42c037475a907c874a38b062d))

* chore: add links to API ([`b7a94df`](https://github.com/relay-md/relay.md/commit/b7a94df53f7044d71cec0f7355fd166ba987dc48))

* chore: improve default permissions ([`4ebdf8a`](https://github.com/relay-md/relay.md/commit/4ebdf8a3e6b4c73d531a71bea55f5e25bf5725e7))

* chore: add link to contact form ([`3fbcb93`](https://github.com/relay-md/relay.md/commit/3fbcb93c1b535112b475091715afcc133a071045))

* chore: finish implementation of permissions ([`0137617`](https://github.com/relay-md/relay.md/commit/0137617976999947a24c9dbe2d6343919f16a6ff))

* chore: faq in pricing ([`e2b8b87`](https://github.com/relay-md/relay.md/commit/e2b8b87a9e268cdd3a04cd150e5864456df9e729))

* chore: improve team name validation ([`4d62d69`](https://github.com/relay-md/relay.md/commit/4d62d69de8f118791de30d1847be8ef5188de79d))

* chore: updates to tos ([`3c62d17`](https://github.com/relay-md/relay.md/commit/3c62d1739eaafc467d7be69f0091e2e65a652842))

* chore: minor cleanups ([`c8f5c3b`](https://github.com/relay-md/relay.md/commit/c8f5c3bf369eabbbf351b862f266489297953629))

* chore: proper migration script ([`8a23cb6`](https://github.com/relay-md/relay.md/commit/8a23cb6dffd939ad980dd4a2f22570109a193495))

* chore: make bucket configurable ([`e4c4921`](https://github.com/relay-md/relay.md/commit/e4c4921435b345aca88affead0fc5ded29699cd5))

* chore(ui): nicer permission management for team ([`6bf0f5b`](https://github.com/relay-md/relay.md/commit/6bf0f5bf3e5297d4178a111ad73d485c148bb716))

* chore: test on get endpoint if read is allowed ([`afc330e`](https://github.com/relay-md/relay.md/commit/afc330e506955d52af3b83382eb9be567599c977))

* chore: mark teams paid and allow clicking through upgrade ([`0b64eb5`](https://github.com/relay-md/relay.md/commit/0b64eb5a4de8a4be597b43fcbcb93649ca29e7c9))

* chore: paid until and removal of payment_plan ([`8acc037`](https://github.com/relay-md/relay.md/commit/8acc0376a307fda93259d12b2d59f5920cb8b11c))

* chore: remove irrelevant invoice_id ([`a85610d`](https://github.com/relay-md/relay.md/commit/a85610d38a4c644a20d8820663b99b211874d79f))

* chore: nicer presentation of user in team invite list ([`0af5808`](https://github.com/relay-md/relay.md/commit/0af58085654c3588d382a2cad3ac2e65c5a429f1))

* chore: nicer front page ([`4349e43`](https://github.com/relay-md/relay.md/commit/4349e4372f63b53a79a1906ed054cb41b57f78f4))

* chore: minor fixes to tos ([`2b5a89c`](https://github.com/relay-md/relay.md/commit/2b5a89c626026281c33761bc6885ef78bd88655d))

* chore: improve js code, add more clis calls ([`1deabfa`](https://github.com/relay-md/relay.md/commit/1deabfa18afe76b23d8ba29c8f1dd52d7835370d))

* chore: extra dependency needed ([`fba5b6a`](https://github.com/relay-md/relay.md/commit/fba5b6a3c21018e5a5ca3e526dbe1f22107bc23e))

* chore: add link to teams to navbar and footer ([`75c3bb2`](https://github.com/relay-md/relay.md/commit/75c3bb276ae0bae88cea16d990afd747105f7217))

* chore: quick readme on teams ([`749bea3`](https://github.com/relay-md/relay.md/commit/749bea3db39aa86c6d405708e3f35cfa0ac9aa57))

* chore: add more links to footer ([`a6fefdc`](https://github.com/relay-md/relay.md/commit/a6fefdc45efb6864a0272ac463a78a77f33cec8f))

* chore: move footer into separate file, add reddit and forum links ([`bbc6935`](https://github.com/relay-md/relay.md/commit/bbc69350b255a68895dc8c7d2c225e1e28c8ca2b))

* chore: nicer footer ([`a1df453`](https://github.com/relay-md/relay.md/commit/a1df45362cb0d6be1dd8b9d0a03e468a197b56ce))

* chore: version endpoint ([`bfcd400`](https://github.com/relay-md/relay.md/commit/bfcd400958068705534c9cfe6552b1b3bb366e63))

* chore: add logo as png ([`1164c1a`](https://github.com/relay-md/relay.md/commit/1164c1af154af0b19c835857e2307bc244573661))

* chore: improve landing page, early access, features and pricing ([`d067bd6`](https://github.com/relay-md/relay.md/commit/d067bd6135a11162a917975a6becb6fadc9d9ea9))

* chore(oauth): store more data, proper indices ([`2b8be4d`](https://github.com/relay-md/relay.md/commit/2b8be4d7542da9b130c46263fcca4a2ec2e59ae2))

### Ci

* ci: change pipeline name ([`b8e88cf`](https://github.com/relay-md/relay.md/commit/b8e88cff6ac9abba9a377ce92c4f8226470ee41e))

* ci: deploy on test env ([`fc16dbe`](https://github.com/relay-md/relay.md/commit/fc16dbe62b2578e3c04cbb9928fb8ece86ed466d))

* ci: better tags for deploy from develop ([`51056f2`](https://github.com/relay-md/relay.md/commit/51056f2cc91f511b412bea23a8458aa5bc840fbf))

* ci: deploy when pushing to develop for faster development ([`cf77ba1`](https://github.com/relay-md/relay.md/commit/cf77ba188dbdf039ee13fa7cae2f52ee09b2e3e0))

* ci: detach from nomad job ([`a51d65a`](https://github.com/relay-md/relay.md/commit/a51d65a433e2243c7e4ea685fcb4710e324adcc3))

* ci: fix deployment variables ([`b1d6bf5`](https://github.com/relay-md/relay.md/commit/b1d6bf5c8344bc9dbc729f125f003ff4b731c9f8))

* ci: fix issue with pipeline loading environment variables ([`7db450c`](https://github.com/relay-md/relay.md/commit/7db450cc6c4827704abf0ad8f3b57fc4aacc37f4))

* ci(drone): test+build on drone ([`cd57088`](https://github.com/relay-md/relay.md/commit/cd570880124e86f4383220297575995d2c8ecc46))

### Feature

* feat: add working docker-compose ([`ef2e0f9`](https://github.com/relay-md/relay.md/commit/ef2e0f9b96334a5861e00c08bc78e92bc843cfb3))

* feat(celery): add basic framework for celery ([`6aba073`](https://github.com/relay-md/relay.md/commit/6aba0736a66bde4aafcd8f0ddcac726335edd826))

* feat: allow to provide a markdown description for team ([`9ba4257`](https://github.com/relay-md/relay.md/commit/9ba425788521f9abbef761aece7495155930935b))

* feat(rate-limits): use redis to support rate-limiting ([`d9bd0fb`](https://github.com/relay-md/relay.md/commit/d9bd0fbb6deeaf641be32dae727b7173cb7255cd))

* feat(session): store sessions in redis db ([`c1f0966`](https://github.com/relay-md/relay.md/commit/c1f0966862f79208ab23de4f89f9583b8ba8f812))

* feat(configure): explicit page to link obsidian ([`ac7d455`](https://github.com/relay-md/relay.md/commit/ac7d4553acd43bea9ab9b78638b4239a3c1c5979))

* feat: remove billing ([`75eb1b0`](https://github.com/relay-md/relay.md/commit/75eb1b048eb7c581fdfe297d13f6feb3b478c437))

* feat: support for folders in filename ([`7fb014a`](https://github.com/relay-md/relay.md/commit/7fb014a8655542a4ba315ebdc946bbee949df077))

* feat(library): list documents from team_topic ([`90cdd86`](https://github.com/relay-md/relay.md/commit/90cdd860fbd17e3692598f279314353e88baaec3))

* feat(v1): additional v1 routes for teams and topics ([`e339a38`](https://github.com/relay-md/relay.md/commit/e339a3870673dcf0bc5464a149faf3a77c7e2d6a))

* feat(library): initial boilerplate for library ([`adb5224`](https://github.com/relay-md/relay.md/commit/adb5224a142d97a9271cb983b10519f863d6736f))

* feat(plugin): more details and hand out the api url via configuration link ([`5d9f711`](https://github.com/relay-md/relay.md/commit/5d9f7110f0656d1582a012c1c2eeb1e261b9d067))

* feat(assets): allow to delete and update assets ([`beb18c7`](https://github.com/relay-md/relay.md/commit/beb18c70a8eba16b882c0b3d68cee8f54794d48d))

* feat(marketing): video demonstrating how it works ([`183a3f2`](https://github.com/relay-md/relay.md/commit/183a3f277a5f56d950f13c85b16f715550fd6dd1))

* feat(rate-limits): implement rate limits ([`498e06d`](https://github.com/relay-md/relay.md/commit/498e06d09e26949e6f4458a8d382e44574a733a2))

* feat(prerender): make use of prerender to show documents ([`2e59a8d`](https://github.com/relay-md/relay.md/commit/2e59a8d3a6954e896520e0bab800488cc03cd159))

* feat: list news sites in sitemap ([`d8a18fe`](https://github.com/relay-md/relay.md/commit/d8a18fed34bf7c754cde029a5dff3b2afd93675c))

* feat(assets): initial api implementation for get asset ([`2b451df`](https://github.com/relay-md/relay.md/commit/2b451df63b66c5aa415ccb9f2f5f39b6041c98d9))

* feat(assets): implement basic asset support ([`bc4b061`](https://github.com/relay-md/relay.md/commit/bc4b061ba303ec3e6c7affc8fc1c303e337385e1))

* feat: separate onboarding stage to have tos/privacy confirmed ([`dee3010`](https://github.com/relay-md/relay.md/commit/dee30107a6f57e88045c6234747fa04d5370d881))

* feat(pricing): any change to public perms requires payment ([`fa2dd53`](https://github.com/relay-md/relay.md/commit/fa2dd5377965c544a02f9ae137f1f5a145e10a26))

* feat(htmx): searchable topics ([`be0f8b3`](https://github.com/relay-md/relay.md/commit/be0f8b30c5570a8097f44a47d0d09da702c85da5))

* feat(sitemap): initial implementation of sitemap ([`76993b9`](https://github.com/relay-md/relay.md/commit/76993b9f0d2d506b5e8897625e3615660a873f72))

* feat(esbuild+sass): make better use of web tools instead of loading external assets ([`94ba669`](https://github.com/relay-md/relay.md/commit/94ba6691c20389deb790929f2f175885a4075fd9))

* feat(matomo): add tracking code ([`fa11c00`](https://github.com/relay-md/relay.md/commit/fa11c001c6bbde6f17beb059ca812391cc65b555))

* feat(teams): selected teams, search for teams ([`c458f7f`](https://github.com/relay-md/relay.md/commit/c458f7f423702e5ab4bf2243dc1c1d57cba77303))

* feat(subscription): deal with subscriptions using stripe webhooks ([`c0f0ae5`](https://github.com/relay-md/relay.md/commit/c0f0ae55e00d52e9e214fa75cb4416cc650cb128))

* feat(seats): implement seats for subscription ([`7a3e53a`](https://github.com/relay-md/relay.md/commit/7a3e53aa08da311c6cb623cb2f67e14a500f5f5d))

* feat(contact form): add a contact form ([`5af5d80`](https://github.com/relay-md/relay.md/commit/5af5d80b29f352e82ed370f7c85cbd568d6e3ce5))

* feat(perms): require read/post for unpaid teams ([`9df1e53`](https://github.com/relay-md/relay.md/commit/9df1e53773935cd2589dd85771f8be46ecd47c50))

* feat(team): allow to hide a team ([`8838468`](https://github.com/relay-md/relay.md/commit/8838468c7edba92dd4caf3024562d8a693b52ed3))

* feat(pug): consistently use pug over html templates ([`d63086a`](https://github.com/relay-md/relay.md/commit/d63086a68c9be2150735aef530e6067c728e8c41))

* feat(stripe): offload stripe specifics into separate tables ([`ef14b58`](https://github.com/relay-md/relay.md/commit/ef14b5854bbd55405955df465d02a696f99153d3))

* feat: sort teams by members ([`48eb0d8`](https://github.com/relay-md/relay.md/commit/48eb0d8e26255fe034035887f5d5b96be095d5d6))

* feat(susbcriptions): run the numbers by users per team ([`3f80d3d`](https://github.com/relay-md/relay.md/commit/3f80d3dee647ca0823d636f78d0d9fec0902a2cd))

* feat(permissions): implement highly flexible permissions scheme ([`11b2279`](https://github.com/relay-md/relay.md/commit/11b22791d5a718f47fb8850e196084c03e4396d1))

* feat(permissions): initiate implementation of permissions scheme ([`c027c34`](https://github.com/relay-md/relay.md/commit/c027c340816cdb5908a4cf822e3542a88aceff1e))

* feat(billing): dropin payment via adyen ([`41de7b9`](https://github.com/relay-md/relay.md/commit/41de7b9f885f4849229924a3aed3b8381821923d))

* feat(billing): support subscription billing ([`6ac66ff`](https://github.com/relay-md/relay.md/commit/6ac66ff463f8739e386877f91cc2ef11385001af))

* feat(billing): implement basic payment flow ([`9937a4a`](https://github.com/relay-md/relay.md/commit/9937a4abd75b67d36a0fab9304427b31e318bc9d))

* feat(billing): initial billing with checkout.com ([`c718b32`](https://github.com/relay-md/relay.md/commit/c718b32a18038937f295b6d9ba178834cfe8902b))

* feat(pricing): custom pricing page~ ([`d65d957`](https://github.com/relay-md/relay.md/commit/d65d9575599335a4a38fac7a332071da67081985))

* feat: user profile picture ([`7142ccb`](https://github.com/relay-md/relay.md/commit/7142ccb45bc5df1a752f5ef3d69f259904cdc23d))

* feat(news): nicer news page ([`cfd71dd`](https://github.com/relay-md/relay.md/commit/cfd71ddadf96fc94c1efeecb8795daf5faf96c4f))

* feat(news): initial work on news site ([`a2ca506`](https://github.com/relay-md/relay.md/commit/a2ca506dde8a34ecf87fc89d50524a86a0ea1489))

* feat: allow to use markdown in pug ([`9d186f0`](https://github.com/relay-md/relay.md/commit/9d186f028f1e5eb1a78a0f05c03c2b0d34f9bc0e))

* feat: allow to select oauth provider (google, github) ([`9033933`](https://github.com/relay-md/relay.md/commit/9033933d3f76d3b9e8a5f0c4d669e22c0248a38c))

* feat: show oauth provider when listing users ([`692318c`](https://github.com/relay-md/relay.md/commit/692318c6538c0f058892b30afaa1ce063dfdd9d5))

* feat: force google users to provide a username ([`777181f`](https://github.com/relay-md/relay.md/commit/777181f20bbd3b350f44b1190af35b2ba9e7f4a6))

* feat: oauth via google ([`0d36526`](https://github.com/relay-md/relay.md/commit/0d36526df32293310e3476e3f70e8e6f2672a2fc))

* feat(pydantic-v2): migration to pydantic v2 ([`3f729b1`](https://github.com/relay-md/relay.md/commit/3f729b108f4eeebd868c30907ecd8ce57ec76a73))

* feat: list of members in a team ([`4c1a1db`](https://github.com/relay-md/relay.md/commit/4c1a1db14db03962c06e29af9095b48e07fabd12))

* feat: invite users to a team ([`e49bd1c`](https://github.com/relay-md/relay.md/commit/e49bd1c162c47622ec50ab8e0ed326588af46fa2))

* feat: allow to post documents for members ([`4c525cf`](https://github.com/relay-md/relay.md/commit/4c525cfd85974865a4ae523e3ad860a19cde9a62))

* feat: explanation for relay-title ([`61d16da`](https://github.com/relay-md/relay.md/commit/61d16da990eb820ea054e23ab6f111ce8e5e2889))

* feat(pagination): paginate on separate documents page ([`523f559`](https://github.com/relay-md/relay.md/commit/523f559c33b13d91f0bf20b77e67702af22020ec))

* feat(join): allow a user to join a team, prevent posting to restricted or private teams ([`8975fd2`](https://github.com/relay-md/relay.md/commit/8975fd26d122aed3766d1f029f08392f50113ab1))

* feat(team-membership): enable to be part of a team, indpendent of subscriptions ([`ce89522`](https://github.com/relay-md/relay.md/commit/ce89522d61f78c879e3cce2396c1c35af03a91b1))

* feat: more flexible team.type ([`1cfd902`](https://github.com/relay-md/relay.md/commit/1cfd90286f534b36c36040ecf935b145a10ac790))

* feat: automatically subscribe to news@relay.md ([`4983140`](https://github.com/relay-md/relay.md/commit/4983140d24daad46f82d103fea380211afe81acb))

* feat(web): dark/light switcher ([`2dc7269`](https://github.com/relay-md/relay.md/commit/2dc72699085bc781498d0ec92a9fa91d188475ff))

* feat: store documents in subfolders on minio ([`83c4f45`](https://github.com/relay-md/relay.md/commit/83c4f45661776163c712a447e90ea7f02ce1cb42))

* feat(title): store document title in database ([`efad9a8`](https://github.com/relay-md/relay.md/commit/efad9a86b97f9fd61232571156ae911cb6906e79))

* feat: proper testing for subscriptions and listing of posts ([`b8aa95a`](https://github.com/relay-md/relay.md/commit/b8aa95ab710a67eae3a7f07d1727a39e30b6eaab))

* feat: allow to subscribe to team/topics ([`98eebe5`](https://github.com/relay-md/relay.md/commit/98eebe5181aa4a37f6c2eeb8d4e412f6c31e026d))

* feat(cli): more powerfull cli tools ([`5f09225`](https://github.com/relay-md/relay.md/commit/5f09225ed0f2f6e008474abd4b8f0acf161ed2d0))

* feat: include prometheus exporter ([`e7ba269`](https://github.com/relay-md/relay.md/commit/e7ba269201657d1943652b25c0ca8e8d727add06))

* feat(hijs): code highlighting in viewer ([`f855b9b`](https://github.com/relay-md/relay.md/commit/f855b9b6463b301d93623bc433bc3b9d301df6eb))

* feat: allow to read public docs without api-key ([`0d721ef`](https://github.com/relay-md/relay.md/commit/0d721ef28b257b55c15c7d637e0a4b277b103433))

* feat: deal with redirects during auth/login/register etc ([`96f2aa1`](https://github.com/relay-md/relay.md/commit/96f2aa13ad7d564e1606c899367ef3f1f0b7733d))

* feat: allow to configure obsidian with a single click ([`9d1f15f`](https://github.com/relay-md/relay.md/commit/9d1f15fd2ca48bde05fa98f9c5c831a113f294eb))

* feat: explain attributes, list teams ([`d7caa2b`](https://github.com/relay-md/relay.md/commit/d7caa2be4a165f9b812f390a9a6b54446f3eeba3))

* feat: public docs and read-password ([`2d6c4c8`](https://github.com/relay-md/relay.md/commit/2d6c4c836742e2d4035521c59b24b8165e7ac2f3))

* feat(web): a site that explains how to install the plugin ([`4b0c2ba`](https://github.com/relay-md/relay.md/commit/4b0c2ba137a1d53cacae0ede97fd242bf3406651))

* feat: how it works ([`509efec`](https://github.com/relay-md/relay.md/commit/509efeccaf49dda5c2744fd7c616468a0a5ec011))

* feat: allow sharing docs with users ([`31c6711`](https://github.com/relay-md/relay.md/commit/31c6711ca507f62ed3d63e3d4c959345136e165e))

* feat: initial work on permission scheme ([`aec0022`](https://github.com/relay-md/relay.md/commit/aec002201e734741c39c8e0078b587a9e0ad2141))

* feat(put): allow to put an entire object ([`f6414ea`](https://github.com/relay-md/relay.md/commit/f6414ea87ba665b48d2a24c359de0cacb569036c))

* feat(health): check endpoint on web ([`fecbd81`](https://github.com/relay-md/relay.md/commit/fecbd81d289ddcd78ffe9c5a96bf972f0edc7077))

* feat(tests): api tests happy path ([`6381bec`](https://github.com/relay-md/relay.md/commit/6381becc4b55dae1e0b67aa358e04b7d56bca3bc))

* feat(health): health endpoint and initial testing ([`f9ba732`](https://github.com/relay-md/relay.md/commit/f9ba73290f72328302a86542eea5a73fb3559d52))

* feat(profile): initial work for profile ([`8d73e4d`](https://github.com/relay-md/relay.md/commit/8d73e4de0dc276c4b5eb63d29c9ffa3f15df340b))

* feat(viewer): initial implementation for viewer ([`4f4542f`](https://github.com/relay-md/relay.md/commit/4f4542f28d3d940ebb86c3cc88a19f97fcf04ca6))

* feat(web): host homepage on backend as well ([`453359a`](https://github.com/relay-md/relay.md/commit/453359ae53ec563a4825b699b2bcbf09a7e4e7f1))

* feat: obtain recent docs, allow specify filename in frontmatter ([`1870c18`](https://github.com/relay-md/relay.md/commit/1870c185367b374b440b7aca6c59ce2872d4dfe2))

* feat: allow to obtain raw text/markdown payload ([`a69f9e1`](https://github.com/relay-md/relay.md/commit/a69f9e14d8b91cb5829230d17ca0092f7b0735f6))

* feat(minio): upload and get documents from minio/s3 ([`505db8c`](https://github.com/relay-md/relay.md/commit/505db8c03f0c981ca1c29323ca35ed664efff67c))

* feat: disable openapi url for web interface ([`c29477b`](https://github.com/relay-md/relay.md/commit/c29477b3c62b4109104dad2f6f88196a20cd17e4))

* feat(cli): modulerize cli tools ([`d6960e9`](https://github.com/relay-md/relay.md/commit/d6960e99fb67a16a2375ca80e2f0bcd4200de740))

* feat: distinct web module ([`cb898fa`](https://github.com/relay-md/relay.md/commit/cb898fad6b0e2995dba662dd16a6f69a5fb7ff7d))

### Fix

* fix: proper testing of modify permissions ([`196a69c`](https://github.com/relay-md/relay.md/commit/196a69c10a9df698875a96d5da7481a9f7d1993e))

* fix: do not show None ([`aa04f87`](https://github.com/relay-md/relay.md/commit/aa04f877d26ff393ac3ecd1e8b9143114c19edc6))

* fix: optionally join the news@relay.md team ([`41c6a06`](https://github.com/relay-md/relay.md/commit/41c6a0636b8ed583e56e490afd22a5d9c3a3ca58))

* fix: contact form needs to use the email address in from field ([`d39d953`](https://github.com/relay-md/relay.md/commit/d39d953dc3efa7ddf3d8a54da7e319fbc5723e5c))

* fix: ensure we only return a document once ([`7b74329`](https://github.com/relay-md/relay.md/commit/7b743299df4a9eeaed6ffaf393c7bab8aa38b986))

* fix: allow extra vars in .env ([`ae9ea71`](https://github.com/relay-md/relay.md/commit/ae9ea71dd5f0f0880511b451daabbbac2a0d1eb8))

* fix: add missing file ([`33e7886`](https://github.com/relay-md/relay.md/commit/33e788614b43b006194fd101a93fcc2ea85a18e0))

* fix: lint ([`aae5a7e`](https://github.com/relay-md/relay.md/commit/aae5a7ec084eb124e4b6146890e118b1136c9ab5))

* fix: use table for document library ([`df8e4b8`](https://github.com/relay-md/relay.md/commit/df8e4b892f9174d27b6c3ba56e8be4ac4276d0e5))

* fix: consistency w.r.t. spacings ([`5802a67`](https://github.com/relay-md/relay.md/commit/5802a67e2e449cb1d334e7ece3aad008fc564349))

* fix: typo when merging ([`80fbc94`](https://github.com/relay-md/relay.md/commit/80fbc94d5f0770dca1a028f2f3f7152e7936c40f))

* fix: typos ([`593cd63`](https://github.com/relay-md/relay.md/commit/593cd636da301eafc7537a40da3c038531fd87f9))

* fix: typo ([`051ab2f`](https://github.com/relay-md/relay.md/commit/051ab2f3e08a264b1353bf79ea984f36075907f8))

* fix: sitemap for googlebot ([`85f3ae5`](https://github.com/relay-md/relay.md/commit/85f3ae5eaf64ccce10f3c8df5a0d5501d5eb4efa))

* fix: linting ([`70d5ba8`](https://github.com/relay-md/relay.md/commit/70d5ba8c8b70d9307c34fae797dbe06647fab4d6))

* fix: issue with stripe integration ([`82f49d2`](https://github.com/relay-md/relay.md/commit/82f49d2446864edcd3f280b6e405d648402abf16))

* fix: more flexible way to skip prerender for paths ([`b155cea`](https://github.com/relay-md/relay.md/commit/b155ceaf025f289022ef92de82a3554d07085c6d))

* fix: typo ([`79644fa`](https://github.com/relay-md/relay.md/commit/79644fac3506d622376da366bfa593bb9838e2e7))

* fix: sitemap for googlebot ([`506b232`](https://github.com/relay-md/relay.md/commit/506b232b02dc0958f0d7b83e140d5dd11c2642a3))

* fix: missing quotes ([`b79a5c4`](https://github.com/relay-md/relay.md/commit/b79a5c4bec766281feed083b4d0272dc52c08cd6))

* fix: improve stripe billing and add unittests ([`cb403d9`](https://github.com/relay-md/relay.md/commit/cb403d939898f58bc3740e22626999223820c834))

* fix: recurrring payments typo ([`3839c7d`](https://github.com/relay-md/relay.md/commit/3839c7d2bd48c5bee89d0d34d2d015755a2b2339))

* fix: need to obtain email for github through additional request ([`88bbec4`](https://github.com/relay-md/relay.md/commit/88bbec407ba82a739a9e6206faa6cb481d5bec54))

* fix: unittests ([`8e05a86`](https://github.com/relay-md/relay.md/commit/8e05a86fe45b63171e9f450c3c569420e57e2ae6))

* fix: unittests no longer can test x-relay-* attributes ([`9e511a6`](https://github.com/relay-md/relay.md/commit/9e511a656cb991465a566599e08663b519655f3f))

* fix(billing): an additional activation path fr the subscriptin ([`c991f5a`](https://github.com/relay-md/relay.md/commit/c991f5a48359db986eb40c771d1ede2b699e1e2b))

* fix: set initial datetime for access token to 2020 ([`d47570f`](https://github.com/relay-md/relay.md/commit/d47570fb4c0fe4a880fed938cdc54c842d79b9da))

* fix: layout.pug had wrong intendation and missing tag ([`2f47ce8`](https://github.com/relay-md/relay.md/commit/2f47ce8911b254363927f6633c271d3cfb49bddb))

* fix: js functions were unavailable in browser ([`bc06e46`](https://github.com/relay-md/relay.md/commit/bc06e460903234d31c80b6a1c703ec54501a57ea))

* fix: sitemap.xml format was not accepted by google due to datetime and missing namespace ([`d4a0715`](https://github.com/relay-md/relay.md/commit/d4a0715012c1780bc29798fcd7bfbd387520f385))

* fix: typo ([`6455051`](https://github.com/relay-md/relay.md/commit/6455051e1678ef81a429b9cb65a46dcf4a17158b))

* fix: more meta details in layout ([`597096e`](https://github.com/relay-md/relay.md/commit/597096e3a4fa85520954c6023486e874292716a5))

* fix: target: _blank with noopener ([`c8bf0d3`](https://github.com/relay-md/relay.md/commit/c8bf0d37d3712ae8043170f70a669fd6e865afa2))

* fix: team hide is a premium feature, really ([`9f1adec`](https://github.com/relay-md/relay.md/commit/9f1adec74382b5f0dbfada9f898ff1157635296e))

* fix: ensure we have the required files handy, even if empty (requires build with esbuild) ([`e2e5edf`](https://github.com/relay-md/relay.md/commit/e2e5edfedc4f84a03bfd1bac22953003ddd95a1f))

* fix(seo): make requested changes to layout ([`9be9639`](https://github.com/relay-md/relay.md/commit/9be9639781a89480bb34f0109034faf6b1baf9e4))

* fix: remove early access terms ([`593ae5b`](https://github.com/relay-md/relay.md/commit/593ae5b9e1ba919b6d2f58c3082fc96b3733cdde))

* fix: public documents do not require checks to read ([`d8173f9`](https://github.com/relay-md/relay.md/commit/d8173f947d9af9d64c8da6b9c853a5b26e632822))

* fix: team list with headline looks better now ([`fbaff14`](https://github.com/relay-md/relay.md/commit/fbaff14b3facccec4eaabf1fbc6c011119bd7772))

* fix: make sentry optional ([`c36799b`](https://github.com/relay-md/relay.md/commit/c36799be4d3f4942c2c236716e6cb8673a6687f1))

* fix: tests ([`babba50`](https://github.com/relay-md/relay.md/commit/babba5059c4830dfc9c141ee87e4679a65b435e9))

* fix: require a github username for oauth ([`4986a17`](https://github.com/relay-md/relay.md/commit/4986a178bd131ec585a88880bdf9a23216a82197))

* fix: additional test for empty upload ([`4d4b289`](https://github.com/relay-md/relay.md/commit/4d4b289e7b5363ca824de3ea81e9523c051f4101))

* fix: linting ([`52b3513`](https://github.com/relay-md/relay.md/commit/52b35135c16548e9f7c28642f477b844632e98e7))

* fix: unittests ([`c7e6334`](https://github.com/relay-md/relay.md/commit/c7e633430d32e7f3b63a7d2b9314dee4b850ab62))

* fix: obtain emails thru api in case profile has no default email ([`4078ed7`](https://github.com/relay-md/relay.md/commit/4078ed76960a63bddeb71be4c26daa9285e04b08))

* fix: only activate a subscription if it gets paid ([`eb7a55e`](https://github.com/relay-md/relay.md/commit/eb7a55e4500ed82e58d9a2e7cfcea09bcdb49141))

* fix: default seats=1 ([`d9a3285`](https://github.com/relay-md/relay.md/commit/d9a3285d95c128c9ba4677ec889856977566afcc))

* fix(stripe): submit the customer id in the session ([`c4f0cfd`](https://github.com/relay-md/relay.md/commit/c4f0cfd9185cdfc9e7cce530f300bae58d15b68c))

* fix(stripe): proration_behavior invalid here ([`a02c73f`](https://github.com/relay-md/relay.md/commit/a02c73f6acd175923803ce012774a3eede184f41))

* fix: obtain access_token from doc, linting ([`078ec6c`](https://github.com/relay-md/relay.md/commit/078ec6c5c365644798ad237f7b18e145767ea4a0))

* fix: typo ([`de7840f`](https://github.com/relay-md/relay.md/commit/de7840fdedbc8d0bfb3b857d7748f9c09fa0bfad))

* fix: typo ([`16c7df6`](https://github.com/relay-md/relay.md/commit/16c7df68206ea9b232ca72e4e4d9fb27da2b064f))

* fix: unittests ([`9c1bbf8`](https://github.com/relay-md/relay.md/commit/9c1bbf8442ca94aeceecc2233dd04090b09be518))

* fix(billing): properly deal with subscription periods ([`9b50715`](https://github.com/relay-md/relay.md/commit/9b507156aff61556beb80387f5b8f05d72818235))

* fix: proper subscription handling with price ([`3d4520d`](https://github.com/relay-md/relay.md/commit/3d4520d2cc53fd4839bfc8f3fd4e774364a6815f))

* fix: permissions and list of teams with no members ([`bd72164`](https://github.com/relay-md/relay.md/commit/bd72164c1d83a6cee7acd67708e1341f090e9613))

* fix: unittests ([`a14eed1`](https://github.com/relay-md/relay.md/commit/a14eed1c52627e92165ab660ccf7ec2fe2445d38))

* fix: proper redirect ([`95de82d`](https://github.com/relay-md/relay.md/commit/95de82dfe4f67875000c4f6bd7868f07606bb40b))

* fix: database must do pre_ping by default ([`902a11a`](https://github.com/relay-md/relay.md/commit/902a11a1f0b1e9718749e30ad7bdcac52c985a50))

* fix: proper payment return URLs ([`19952b9`](https://github.com/relay-md/relay.md/commit/19952b9f36e731d1cf74ce93a448dc8681a544db))

* fix: cyclic import error resovled ([`9ef3017`](https://github.com/relay-md/relay.md/commit/9ef3017b77e381e0a45b022a8ceece91ecfaf8e9))

* fix: unittests ([`712d1d1`](https://github.com/relay-md/relay.md/commit/712d1d14abaf747fc4802decd788c3a82e45130c))

* fix: add HMAC and favicon ([`78ddf78`](https://github.com/relay-md/relay.md/commit/78ddf7819ea4b70bd5f75f3c78491f9acd349df0))

* fix(tos): more text ([`74b9fd7`](https://github.com/relay-md/relay.md/commit/74b9fd7743bfe29e97ded938f30e6a3b0f55e19f))

* fix: email validation ([`d05e1df`](https://github.com/relay-md/relay.md/commit/d05e1df78dc16c46dada5514108cb0d8c1ca5416))

* fix: remove TeamType from table and code ([`a67891c`](https://github.com/relay-md/relay.md/commit/a67891c431dd69debcaa1560c6cc93f74c1bd579))

* fix(ui): removal of restricted ([`a6b6e06`](https://github.com/relay-md/relay.md/commit/a6b6e068e6577dd97dc38d6ff221ce84345446d6))

* fix: nicer presentation in ui ([`96570e2`](https://github.com/relay-md/relay.md/commit/96570e2e52304a73497e994776badeb7eff8336d))

* fix: unittests ([`2cb9058`](https://github.com/relay-md/relay.md/commit/2cb9058117ca61f2a02f4552e038e30eb76f37cb))

* fix: unittests ([`39fcd6f`](https://github.com/relay-md/relay.md/commit/39fcd6fa2aa0d184c628e9f4c580950c50228314))

* fix: alembic deals for product sold ([`f1b2f57`](https://github.com/relay-md/relay.md/commit/f1b2f579548bd5b6a830151adc2d659de79737d6))

* fix: move user_id to invoice where it makes more sense ([`6c19b65`](https://github.com/relay-md/relay.md/commit/6c19b6553cfb8ccfcbb07133eab96ab25b8ea30b))

* fix: default value missing for news team topics ([`df90b40`](https://github.com/relay-md/relay.md/commit/df90b409c8954ce736d19697bb8124d03103cc50))

* fix(requirements): downgrade mysqlclient to make docker build again ([`4dec830`](https://github.com/relay-md/relay.md/commit/4dec830bd9376ef21060f6c1fc232967c3a6ee7c))

* fix: add var to tests ([`8238c00`](https://github.com/relay-md/relay.md/commit/8238c004a33e0eb0ee9670d48305eb4251720504))

* fix(requirements): pin mysqlclient so it build in docker ([`df97a5b`](https://github.com/relay-md/relay.md/commit/df97a5bd42dfd32a2624120b63161e8928219da8))

* fix: remove google login for now ([`6cf732f`](https://github.com/relay-md/relay.md/commit/6cf732fb8f6b6c3a1b8cab3b024b8fcf0ddebee0))

* fix: add tos to footer ([`93e5174`](https://github.com/relay-md/relay.md/commit/93e5174b35156bd8a93e707a635110e1af1d38bf))

* fix: tests ([`493e450`](https://github.com/relay-md/relay.md/commit/493e450b99180ff23ba6345285904bfb1aacbe74))

* fix: typo ([`d013184`](https://github.com/relay-md/relay.md/commit/d013184f2813eaf9250d86c88b66b42274b29c64))

* fix: unique constraints on Indices ([`27752bf`](https://github.com/relay-md/relay.md/commit/27752bf69dd7443d40afaa7c0f06c49c6f27ad31))

* fix: flip icons for dark/light mode ([`1fc2209`](https://github.com/relay-md/relay.md/commit/1fc2209dcd8f5eae7a6d03545510791127d40320))

* fix: typing error in py38 ([`e657a77`](https://github.com/relay-md/relay.md/commit/e657a7748b73d344fba3e9e911336645cb20ac3e))

* fix: create documents could be called with string argument ([`003aa25`](https://github.com/relay-md/relay.md/commit/003aa253cf194fb9b284102b85cc133a9865e5e7))

* fix: shared/owned document list in profile ([`5950bd0`](https://github.com/relay-md/relay.md/commit/5950bd0c66fcf04c1b997e8201e748266e522526))

* fix: wrong logic ([`469e381`](https://github.com/relay-md/relay.md/commit/469e381aa19ff267e2f5466450505e06270eee21))

* fix: only show teams when logged or leave early access mode ([`d767cfc`](https://github.com/relay-md/relay.md/commit/d767cfca6f96e1884ad6ef7eedff8b8038d2af19))

* fix: update the datetime on PUT ([`993b95d`](https://github.com/relay-md/relay.md/commit/993b95d107b3fb4902c4834b4ccae8ef1332bd69))

* fix: give frontmatter filename priority over query string ([`cb9b734`](https://github.com/relay-md/relay.md/commit/cb9b734320cc7af26b73f046e40d3f0553fb5c5b))

* fix: unittests need to compliy with new status codes ([`3c49ec8`](https://github.com/relay-md/relay.md/commit/3c49ec880b19afd41024c20ff5fe6aaf589ced1e))

* fix: improve error handling ([`1c6e73b`](https://github.com/relay-md/relay.md/commit/1c6e73bd692bf6421e99c620c47711125c690f8a))

* fix: reuse team.is_private instead of hardcoding _ ([`3c56020`](https://github.com/relay-md/relay.md/commit/3c56020d5c5e769f89b6b18aebfaee2fff9b636c))

* fix: log access to documents ([`dca3115`](https://github.com/relay-md/relay.md/commit/dca311553a329eaf554f0869be8dc23552b3937e))

* fix: remove how it works from navbar ([`95fd349`](https://github.com/relay-md/relay.md/commit/95fd3497cae6f78de4b628e873cea9506454da4d))

* fix: relay_to is now called relay-to ([`55ea950`](https://github.com/relay-md/relay.md/commit/55ea950904fe4c10c740aa9ceaf39c60d0a1e19b))

* fix: viewer obtain documents from public api ([`1a25854`](https://github.com/relay-md/relay.md/commit/1a2585406a2ba20a56d9e9e0a6a42b1d45789e43))

* fix: when properly logged in, show profile link ([`94688be`](https://github.com/relay-md/relay.md/commit/94688bec6b6ea7883cb059e4f67e6f21ea7871ae))

* fix: need config for navbar ([`4e30b5b`](https://github.com/relay-md/relay.md/commit/4e30b5b355b4867dbdf4dbdf59fff72e1c6de5c6))

* fix: forcing release ([`7b3e0db`](https://github.com/relay-md/relay.md/commit/7b3e0dbdad3acb53a1b11e2ae8323ecf58646f61))

* fix: linting ([`c6151db`](https://github.com/relay-md/relay.md/commit/c6151dbd379481b5165e95fc968b850ec195d3d7))

* fix: properly patch minio ([`3fa8392`](https://github.com/relay-md/relay.md/commit/3fa839285cc8c7e89b05e591436d905a4737d799))

* fix: unittests now with relay-document ([`3d2bcd7`](https://github.com/relay-md/relay.md/commit/3d2bcd7a25d41bdf3426f88be0e84faf8e49cfc5))

* fix: remove pricing section ([`77dfa85`](https://github.com/relay-md/relay.md/commit/77dfa8516d5f8ceff0807299d11b7bf4a2f07336))

* fix: more robust uploads, dd document-id ([`845e498`](https://github.com/relay-md/relay.md/commit/845e498086973f91aaaa42766778f2e181eab781))

* fix: import issues when running api and web ([`84f4d98`](https://github.com/relay-md/relay.md/commit/84f4d9810eed075d1857fcc0f297ab1b90044fd8))

* fix: deployment via nomad uses run instead of apply ([`99ece29`](https://github.com/relay-md/relay.md/commit/99ece296b122d9b62aad03ada3efe4a010013c51))

* fix: add mising file ([`efd3f78`](https://github.com/relay-md/relay.md/commit/efd3f7810b36af3a47fbba3e489af440543834f6))

* fix: linting ([`90b4de1`](https://github.com/relay-md/relay.md/commit/90b4de140485c19acbe04c2f66882bd824bde46b))

* fix: unittests should now work ([`59a960b`](https://github.com/relay-md/relay.md/commit/59a960b79091711d474fa50d62f09b176dbf2cc1))

### Refactor

* refactor: simplify database.py ([`65586ea`](https://github.com/relay-md/relay.md/commit/65586ea87bbab1f32ddbae03b0535b00a5e2d5a8))

* refactor: cleanups ([`38f5569`](https://github.com/relay-md/relay.md/commit/38f5569d91502d37107a0b0291f349fd83b35fcf))

* refactor: is_active is_public is_private flags ([`394aed2`](https://github.com/relay-md/relay.md/commit/394aed2e4203ed0a6aa9c0b0e8a0a508da0d96aa))

* refactor: team list nicer ([`c8648e5`](https://github.com/relay-md/relay.md/commit/c8648e5527f0db37d7c69c72e9fedf38a35485bf))

* refactor: separate billing and payment and teams ([`5923d30`](https://github.com/relay-md/relay.md/commit/5923d30bbbff38e056ddb79b1004a426f0e89727))

* refactor: use more pug, fix howitworks, pricelist ([`62676a1`](https://github.com/relay-md/relay.md/commit/62676a1e05fba727b05030cc4eef1074a682aaae))

* refactor: cleanup and stripe integration ([`3645f87`](https://github.com/relay-md/relay.md/commit/3645f876157dbbc33da51981df5363f2bd0504e9))

* refactor: simplify billing ([`8b48c0c`](https://github.com/relay-md/relay.md/commit/8b48c0c7418f2c9df86b0c703dc3ab6a6e16ce93))

* refactor(billing): also subscription claiming works now - ugly tho ([`3a18393`](https://github.com/relay-md/relay.md/commit/3a1839374652e230b83192485cc1b49e69363d16))

* refactor: implementation details for pricing ([`6c98c87`](https://github.com/relay-md/relay.md/commit/6c98c870beb44041430121d7b120df4384b30299))

* refactor(billing): database model for invoicing ([`9966c2e`](https://github.com/relay-md/relay.md/commit/9966c2e3d09c4f37c002e232478cd39ff9667f3b))

* refactor(setup): better dealing with dev population ([`f838891`](https://github.com/relay-md/relay.md/commit/f8388912915e29658becc85377c34ccb4618db8a))

* refactor(tos): ai-ified terms of service, privacy data and imprint ([`5dbf145`](https://github.com/relay-md/relay.md/commit/5dbf145035807eb611ac555431e0b5d6c777a5ca))

* refactor: get_config, overload in conftest ([`f8c74ed`](https://github.com/relay-md/relay.md/commit/f8c74ed8347e156d73a67b5e23cb4dce3334d5e7))

* refactor: some cleaning up ([`cd4cb41`](https://github.com/relay-md/relay.md/commit/cd4cb41b621c40ec2841b1b20dbda0b62b1c5e53))

* refactor: remove dulpicate code ([`487dbbf`](https://github.com/relay-md/relay.md/commit/487dbbf756acfe8b1c3f10c83147fe40fb736a1f))

* refactor: more flexible oauth clients ([`35a0b79`](https://github.com/relay-md/relay.md/commit/35a0b79a6a5d8252d2d9b929e0eec96620f39dfe))

* refactor: tests better now ([`2f47c89`](https://github.com/relay-md/relay.md/commit/2f47c89844aef9e84bfe9819cddbbfe3903e7b46))

* refactor: use backend instead of api for project root module ([`1c82e3c`](https://github.com/relay-md/relay.md/commit/1c82e3c299c3e543f220a7d12008ec619d086cb5))

### Unknown

* wip: docker-compose ([`1c21f84`](https://github.com/relay-md/relay.md/commit/1c21f840c121f207d8e4a34f7a2ab73b125db00a))

* Add configure screen ([`a184a4a`](https://github.com/relay-md/relay.md/commit/a184a4ad89811855ae7e22bd6ec37cb85ecbee22))

* Merge pull request &#39;feature/library&#39; (#51) from feature/library into develop

Reviewed-on: https://git.chainsquad.com/knowledgemd/backend/pulls/51 ([`af3a8da`](https://github.com/relay-md/relay.md/commit/af3a8da85d7441fd27bdb3a1b3872e21d31c642f))

* Update backend/models/billing.py ([`1893f93`](https://github.com/relay-md/relay.md/commit/1893f9396e9b0c0a498d28aee55ef39f2fe867f4))

* include code removed before ([`761b814`](https://github.com/relay-md/relay.md/commit/761b814ea3e0ef70f3ec594e0996a45d16e09f19))

* Merge remote-tracking branch &#39;origin/feature/assets&#39; into develop ([`6ff5bb8`](https://github.com/relay-md/relay.md/commit/6ff5bb80e52f0bf9564b521b063f8711edb57323))

* Merge branch &#39;feature/sitemap&#39; into develop ([`17f3478`](https://github.com/relay-md/relay.md/commit/17f347843d3971ba6d33e83c88ba93b5e34992aa))

* Merge branch &#39;feature/seo&#39; into develop ([`d648995`](https://github.com/relay-md/relay.md/commit/d6489957f8ea471b8edd6cbba6ca13ce5cadf86f))

* Merge branch &#39;feature/billing&#39; into develop ([`f72e065`](https://github.com/relay-md/relay.md/commit/f72e065cf129ea6d91b2d7291b75aa595ca29fa3))

* wip: ([`00a8b7e`](https://github.com/relay-md/relay.md/commit/00a8b7ed63418b4edb98cc888b45dcd48ecffc8c))

* wip: play around with adyen subscriptions ([`1f43089`](https://github.com/relay-md/relay.md/commit/1f43089cb6db21c4314ac0b4e843852b75b27232))

* refactoring: pricing and routes ([`25d1ee9`](https://github.com/relay-md/relay.md/commit/25d1ee96625a8a76f2818c60b7b3597fdfd9c76d))

* Merge branch &#39;feature/news-site-requires-document-title&#39; into develop ([`0462edb`](https://github.com/relay-md/relay.md/commit/0462edb0678ffe9813e9d09cc1a5fef340e0fdad))

* bump(deps): update some dependencies ([`493709e`](https://github.com/relay-md/relay.md/commit/493709ed2edcd400957aef27c5f416f24a856cd1))

* Revert &#34;ci: deploy when pushing to develop for faster development&#34;

This reverts commit cf77ba188dbdf039ee13fa7cae2f52ee09b2e3e0. ([`1b0a11b`](https://github.com/relay-md/relay.md/commit/1b0a11b3b26e819aa04932186ab7072948245814))

* Revert &#34;ci: better tags for deploy from develop&#34;

This reverts commit 51056f2cc91f511b412bea23a8458aa5bc840fbf. ([`23cfc5f`](https://github.com/relay-md/relay.md/commit/23cfc5ffa0a56dbadeba719e790badd9d926caf3))

* First initial release

BREAKING CHANGE: After this release, the database needs migrations ([`a5ee045`](https://github.com/relay-md/relay.md/commit/a5ee0453679841fec0b063157efb222ddf2f36ac))

* lint: rerun black on all files ([`e9f54d7`](https://github.com/relay-md/relay.md/commit/e9f54d77e27858e5f6edb1052bc23f72ead0fb6c))

* ops(alembic): import from correct module ([`4280954`](https://github.com/relay-md/relay.md/commit/4280954cf0ac3bc43193c1a0ae584bc556545dca))

* bump: requirements + more output in header ([`b3e67b3`](https://github.com/relay-md/relay.md/commit/b3e67b321fbf95d0cb74a2f6fd3c55ac3b6d1f94))

* initial work on s3 integration ([`01769cf`](https://github.com/relay-md/relay.md/commit/01769cf6f4da91862189244679090e016cf2e201))

* bunch of work ([`d557a45`](https://github.com/relay-md/relay.md/commit/d557a450773b160745cd136f085b8e2b7bf7150d))


## v0.1.2 (2023-11-13)

### Fix

* fix: another release triggered by drone hopefully ([`c286f8b`](https://github.com/relay-md/relay.md/commit/c286f8bf558112dca66fc46f0b0c7c634836272f))

### Unknown

* 0.1.2

Automatically generated by python-semantic-release ([`0259b7c`](https://github.com/relay-md/relay.md/commit/0259b7c1e929209f63f973bb4456d729b22befca))


## v0.1.1 (2023-11-13)

### Fix

* fix: proper pipelining with release ([`8dc69a1`](https://github.com/relay-md/relay.md/commit/8dc69a1411826dffcea9f3deb1444fa477812264))

### Unknown

* 0.1.1

Automatically generated by python-semantic-release ([`c683e10`](https://github.com/relay-md/relay.md/commit/c683e108102669e029418db66dcda84f7efad675))


## v0.1.0 (2023-11-13)

### Ci

* ci: run drone-&gt;docker only on tags ([`ed0d59b`](https://github.com/relay-md/relay.md/commit/ed0d59b6ce3377e88f7f65f3ce55d40939694b41))

* ci: drone config ([`42969d1`](https://github.com/relay-md/relay.md/commit/42969d1f663ae4998708e01f4ffb2cbe92025d0d))

### Feature

* feat: add cors ([`5b6c799`](https://github.com/relay-md/relay.md/commit/5b6c7990af17e271cbb7ed0f9e07bee7b3011944))

* feat: use mailchimp ([`365ad29`](https://github.com/relay-md/relay.md/commit/365ad29c5fae44b2569420afc081ed9f1a05c917))

* feat(alembic): upgrade script and new attribtues for landingpageemail ([`a2d37eb`](https://github.com/relay-md/relay.md/commit/a2d37ebe4767040e286625fdae338883cb718c40))

* feat(api): endpoint to confirm email ([`c390432`](https://github.com/relay-md/relay.md/commit/c3904325475723e3647cc10c2b290ad65f183ae6))

* feat: landing page support for channel.md ([`6331714`](https://github.com/relay-md/relay.md/commit/63317146bc459d3d283bdbfc42a4dd161980b7bf))

### Fix

* fix: remove indicator ([`b3a8484`](https://github.com/relay-md/relay.md/commit/b3a848405ed316f1c546c9a545c029039edaf352))

* fix(v0): properly validate email ([`f0531b6`](https://github.com/relay-md/relay.md/commit/f0531b6cc43afa22f017564807405d33cb66a298))

* fix: multipart form ([`1b368ab`](https://github.com/relay-md/relay.md/commit/1b368abba6bc20d98aa0556e140748d5337ed758))

* fix: parse data from form ([`7af1339`](https://github.com/relay-md/relay.md/commit/7af1339a332412521e71490c57fe4297031894bf))

* fix: make this work in docker ([`b3fdffe`](https://github.com/relay-md/relay.md/commit/b3fdffeb9acb9148464cfc4db5caff9f9e0a5e16))

### Style

* style: autoflake ([`d109c5e`](https://github.com/relay-md/relay.md/commit/d109c5e1130b2f701861c45bec6278caf0e4df53))

### Unknown

* relay.md branding ([`204a4be`](https://github.com/relay-md/relay.md/commit/204a4beb0e3ee40b4feb79bb131277511d261f8a))

* initial ([`75696be`](https://github.com/relay-md/relay.md/commit/75696be3cd50da4a4aa9f6023d3313716e165c7d))
