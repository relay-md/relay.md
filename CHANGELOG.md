# Changelog

<!--next-version-placeholder-->

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
