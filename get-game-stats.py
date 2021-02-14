import pandas as pd
import numpy as np
import os
import requests
import time
from download import download_file

# all of my available replays
# https://ballchasing.com/?title=&player-name=pcmcd&season=&min-rank=&max-rank=&map=&replay-after=&replay-before=&upload-after=&upload-before=

urls = []
#1/8 CLMN preseason tournament
urls.append([['dbcb5251-b75c-4e29-a161-38ebde9418d9'],['Week 0'],['Preseason'],['Series 1'],['2021-01-08'],['CLMN']])
urls.append([['9eda6262-6fea-46e2-aa7e-ab4a6d82d0ba'],['Week 0'],['Preseason'],['Series 1'],['2021-01-08'],['CLMN']])
urls.append([['79975f63-9f7e-4120-8102-86bce529bce1'],['Week 0'],['Preseason'],['Series 1'],['2021-01-08'],['CLMN']])
urls.append([['ce507231-65a6-445f-b71f-576529926950'],['Week 0'],['Preseason'],['Series 1'],['2021-01-08'],['CLMN']])
urls.append([['b0bccf89-964c-4006-80f9-a60054198e61'],['Week 0'],['Preseason'],['Series 1'],['2021-01-08'],['CLMN']])
urls.append([['c71bf073-889f-4a2d-81bb-e2923ba1bf32'],['Week 0'],['Preseason'],['Series 1'],['2021-01-08'],['CLMN']])
urls.append([['46ad1fb8-ef84-4246-9d72-87cb8962d5b3'],['Week 0'],['Preseason'],['Series 1'],['2021-01-08'],['CLMN']])
urls.append([['3fa94855-8e96-4de4-aaea-3ccccf60cf72'],['Week 0'],['Preseason'],['Series 1'],['2021-01-08'],['CLMN']])
urls.append([['0b8405e7-24d4-426c-a18f-a3661ba02aae'],['Week 0'],['Preseason'],['Series 1'],['2021-01-08'],['CLMN']])
#1/11 boosty boys scrim
urls.append([['b399c2f1-14c1-4419-9b56-2dcba8038a63'],['Week 0'],['Preseason'],['Series 2'],['2021-01-11'],['CLMN']])
urls.append([['9d053ab6-fd45-4e29-bd90-bdba4dec0629'],['Week 0'],['Preseason'],['Series 2'],['2021-01-11'],['CLMN']])
urls.append([['70ef7a52-6014-4ec4-8f63-63dc526338e8'],['Week 0'],['Preseason'],['Series 2'],['2021-01-11'],['CLMN']])
urls.append([['83518fa7-9bb7-41c0-b192-2c7f7e96ef40'],['Week 0'],['Preseason'],['Series 2'],['2021-01-11'],['CLMN']])
urls.append([['5d3a843a-62c8-46a7-9bd3-c86e754e5a7d'],['Week 0'],['Preseason'],['Series 2'],['2021-01-11'],['CLMN']])
urls.append([['09772d90-acc7-4692-8e2f-fbb81aaf110e'],['Week 0'],['Preseason'],['Series 2'],['2021-01-11'],['CLMN']])
urls.append([['0f11948f-e73d-448d-9a14-bc687e77156c'],['Week 0'],['Preseason'],['Series 2'],['2021-01-11'],['CLMN']])
urls.append([['37cb2c52-676a-4a07-a16f-3605e47beb6b'],['Week 0'],['Preseason'],['Series 2'],['2021-01-11'],['CLMN']])
#1/11 firestorm scrim
urls.append([['d5559778-1a20-4388-9d9b-a7770573d4cd'],['Week 0'],['Preseason'],['Series 3'],['2021-01-11'],['CLMN']])
urls.append([['fabd2bf6-8a6b-4921-a7a8-c545e408df94'],['Week 0'],['Preseason'],['Series 3'],['2021-01-11'],['CLMN']])
urls.append([['93007698-f2b4-4d23-958f-4438153a2570'],['Week 0'],['Preseason'],['Series 3'],['2021-01-11'],['CLMN']])
urls.append([['8db975aa-4ea9-4e65-a8b8-0a9c6b34ce31'],['Week 0'],['Preseason'],['Series 3'],['2021-01-11'],['CLMN']])
#1/13 firestorm scrim
urls.append([['b76a4b9b-4ee5-4acf-932c-0fa552d3df07'],['Week 0'],['Preseason'],['Series 4'],['2021-01-13'],['CLMN']])
urls.append([['4ba80221-4a36-4b3d-a11d-d808c3f51836'],['Week 0'],['Preseason'],['Series 4'],['2021-01-13'],['CLMN']])
urls.append([['3c1bede4-0449-42ed-b4e6-9a20cb3cdc23'],['Week 0'],['Preseason'],['Series 4'],['2021-01-13'],['CLMN']])
urls.append([['bfc92b44-3310-4bf1-99da-e4018b958f33'],['Week 0'],['Preseason'],['Series 4'],['2021-01-13'],['CLMN']])
#1/15 week 0 scrims (only our games)
urls.append([['708f160c-bd3b-435f-aeb9-ac9c7eb618c9'],['Week 0'],['Preseason'],['Series 5'],['2021-01-15'],['CLMN']])
urls.append([['b7b86822-30df-4652-b4d4-26df4b564e7e'],['Week 0'],['Preseason'],['Series 5'],['2021-01-15'],['CLMN']])
urls.append([['02bcc596-2b0e-43d3-b594-086e1f689952'],['Week 0'],['Preseason'],['Series 5'],['2021-01-15'],['CLMN']])
#1/19 duluth scrim
urls.append([['8646c892-b61c-4508-85ed-ea84debea4f6'],['Week 0'],['Preseason'],['Series 6'],['2021-01-19'],['CLMN']])
urls.append([['9d379e43-1fa7-4dee-9fa4-b401cd7386ce'],['Week 0'],['Preseason'],['Series 6'],['2021-01-19'],['CLMN']])
urls.append([['b40638dc-6b6f-4ca3-b904-33022cf33037'],['Week 0'],['Preseason'],['Series 6'],['2021-01-19'],['CLMN']])
urls.append([['be52e085-e6df-4061-8931-af293f306da2'],['Week 0'],['Preseason'],['Series 6'],['2021-01-19'],['CLMN']])
urls.append([['a75dd6d3-0d88-4da9-aea3-661207b2137e'],['Week 0'],['Preseason'],['Series 6'],['2021-01-19'],['CLMN']])
urls.append([['e5baf9d9-499a-44a8-9063-39771bbe060b'],['Week 0'],['Preseason'],['Series 6'],['2021-01-19'],['CLMN']])
urls.append([['a4dc8bec-643a-4cdc-8956-e0fdb39a87c6'],['Week 0'],['Preseason'],['Series 6'],['2021-01-19'],['CLMN']])
urls.append([['f6a11545-62f6-474c-b92a-8da7a1e2d6f4'],['Week 0'],['Preseason'],['Series 6'],['2021-01-19'],['CLMN']])
#1/20 minneapolis scrim
urls.append([['a1e6175c-435c-4a10-aa13-354745b96ff2'],['Week 0'],['Preseason'],['Series 7'],['2021-01-20'],['CLMN']])
urls.append([['c313b774-aef0-4a4d-ba58-b7722f8697f5'],['Week 0'],['Preseason'],['Series 7'],['2021-01-20'],['CLMN']])
urls.append([['774e81d0-7875-4b98-94ba-e65ebe98391e'],['Week 0'],['Preseason'],['Series 7'],['2021-01-20'],['CLMN']])
urls.append([['8bf10bbe-9a9b-43c3-988d-d6c5c9187b16'],['Week 0'],['Preseason'],['Series 7'],['2021-01-20'],['CLMN']])
urls.append([['7dc98c4e-6406-495c-9a3b-65c8a3e6b506'],['Week 0'],['Preseason'],['Series 7'],['2021-01-20'],['CLMN']])
#1/22 minnetonka scrim
urls.append([['e5f81d7f-786e-42b3-859a-582579551f86'],['Week 0'],['Preseason'],['Series 8'],['2021-01-22'],['CLMN']])
urls.append([['d690b8be-b3ab-4479-8fde-0d5acc635624'],['Week 0'],['Preseason'],['Series 8'],['2021-01-22'],['CLMN']])
urls.append([['e11f9f67-e39a-4325-990a-39d8678861d8'],['Week 0'],['Preseason'],['Series 8'],['2021-01-22'],['CLMN']])
urls.append([['1fe48305-2676-40ea-bc68-cff9541dcb85'],['Week 0'],['Preseason'],['Series 8'],['2021-01-22'],['CLMN']])


#1/22 CLMN Regular Season week 1
urls.append([['de9d9a41-7a06-4084-8093-b43ab2ea3d67'],['Week 1'],['Regular Season'],['Series 1'],['2021-01-22'],['CLMN']])
urls.append([['38d4dd5d-6cf3-4554-a826-da2e070776ec'],['Week 1'],['Regular Season'],['Series 1'],['2021-01-22'],['CLMN']])
urls.append([['5c708b5a-2330-4edf-81ed-ba5946be4c5d'],['Week 1'],['Regular Season'],['Series 1'],['2021-01-22'],['CLMN']])
urls.append([['4ff7d3ce-cfab-49c3-8f96-111ac96c5481'],['Week 1'],['Regular Season'],['Series 2'],['2021-01-22'],['CLMN']])
urls.append([['d3cac342-a727-407b-8007-e93364c4b24a'],['Week 1'],['Regular Season'],['Series 2'],['2021-01-22'],['CLMN']])
urls.append([['76bc0f03-373b-41ce-a47a-953db7dbcd93'],['Week 1'],['Regular Season'],['Series 2'],['2021-01-22'],['CLMN']])
urls.append([['de3321cd-253a-42dd-b60c-b129785961d7'],['Week 1'],['Regular Season'],['Series 2'],['2021-01-22'],['CLMN']])
urls.append([['0ac4f9ee-9bd6-432c-8386-e2359834c365'],['Week 1'],['Regular Season'],['Series 2'],['2021-01-22'],['CLMN']])
urls.append([['d4e5f817-0325-4ed1-bf42-b0b46fcd2718'],['Week 1'],['Regular Season'],['Series 3'],['2021-01-22'],['CLMN']])
urls.append([['938ed5ec-298e-493e-bd08-9cd6681145d1'],['Week 1'],['Regular Season'],['Series 3'],['2021-01-22'],['CLMN']])
urls.append([['d768f0eb-d370-4318-8edd-114c67f0e5a5'],['Week 1'],['Regular Season'],['Series 3'],['2021-01-22'],['CLMN']])
urls.append([['049b5978-7c06-461a-b0d9-3c86033692f2'],['Week 1'],['Regular Season'],['Series 4'],['2021-01-22'],['CLMN']])
urls.append([['605e8fa3-5537-4d7b-8803-81fa037a59af'],['Week 1'],['Regular Season'],['Series 4'],['2021-01-22'],['CLMN']])
urls.append([['f01338af-b445-4297-bf1c-7fbd39c8b05b'],['Week 1'],['Regular Season'],['Series 4'],['2021-01-22'],['CLMN']])
urls.append([['321d66b0-4593-4afe-a926-9222d6959265'],['Week 1'],['Regular Season'],['Series 5'],['2021-01-22'],['CLMN']])
urls.append([['2f95aa02-65a5-4d22-9d85-39bd8cd8a4dc'],['Week 1'],['Regular Season'],['Series 5'],['2021-01-22'],['CLMN']])
urls.append([['616e136b-a899-429a-a29b-cd4b6f1acce4'],['Week 1'],['Regular Season'],['Series 5'],['2021-01-22'],['CLMN']])

#1/25 Minneaplolis scrim
urls.append([['3354615d-2a5f-49bd-9f31-f1a3c85ed535'],['Week 0'],['Preseason'],['Series 9'],['2021-01-25'],['CLMN']])
urls.append([['0ea28777-186b-4f31-bf0b-1de444bac563'],['Week 0'],['Preseason'],['Series 9'],['2021-01-25'],['CLMN']])
urls.append([['ac7346e3-9851-430a-b36b-08f1a94739ca'],['Week 0'],['Preseason'],['Series 9'],['2021-01-25'],['CLMN']])
urls.append([['c741e3ac-150d-432d-8e94-37496cecd5c4'],['Week 0'],['Preseason'],['Series 9'],['2021-01-25'],['CLMN']])

#1/28 Firestorm scrim
urls.append([['bf6bb5b0-813a-4368-92fc-8532b53b5783'],['Week 0'],['Preseason'],['Series 10'],['2021-01-28'],['CLMN']])
urls.append([['d2b6db49-6065-4e1e-996d-941dae814434'],['Week 0'],['Preseason'],['Series 10'],['2021-01-28'],['CLMN']])
urls.append([['87b03a5d-7ab7-4100-937a-8dbc88250ce2'],['Week 0'],['Preseason'],['Series 10'],['2021-01-28'],['CLMN']])
urls.append([['9734307a-9b1c-4395-9be1-494edfb477df'],['Week 0'],['Preseason'],['Series 10'],['2021-01-28'],['CLMN']])
urls.append([['e94d94e1-b932-4da9-aa84-a11138eab354'],['Week 0'],['Preseason'],['Series 10'],['2021-01-28'],['CLMN']])
urls.append([['ec235323-7a44-4fa9-bf29-3ead72271b20'],['Week 0'],['Preseason'],['Series 10'],['2021-01-28'],['CLMN']])

#1/29 CLMN Regular Season week 2
urls.append([['71cdcd8c-9c84-4a17-8c46-03d747998223'],['Week 2'],['Regular Season'],['Series 1'],['2021-01-29'],['CLMN']])
urls.append([['5c620611-5779-4715-9186-a518e9c722ae'],['Week 2'],['Regular Season'],['Series 1'],['2021-01-29'],['CLMN']])
urls.append([['89d215ab-a6c8-4264-a5d7-f35b0a892bc0'],['Week 2'],['Regular Season'],['Series 1'],['2021-01-29'],['CLMN']])
urls.append([['7f5bc46a-e482-47f3-b914-74d6c4537b55'],['Week 2'],['Regular Season'],['Series 1'],['2021-01-29'],['CLMN']])
urls.append([['ad9e2c7d-762f-442e-9d5c-049cec70b491'],['Week 2'],['Regular Season'],['Series 1'],['2021-01-29'],['CLMN']])
urls.append([['b80f87fc-c224-4305-a52b-6b3dc79ae21c'],['Week 2'],['Regular Season'],['Series 2'],['2021-01-29'],['CLMN']])
urls.append([['c6ae7701-1468-4820-ab9d-500d3fb13927'],['Week 2'],['Regular Season'],['Series 2'],['2021-01-29'],['CLMN']])
urls.append([['83db2fd0-d488-466b-8867-0de7a1371d70'],['Week 2'],['Regular Season'],['Series 2'],['2021-01-29'],['CLMN']])
urls.append([['5ec0e6ae-010e-4aed-8328-5c50b424e306'],['Week 2'],['Regular Season'],['Series 3'],['2021-01-29'],['CLMN']])
urls.append([['8ce764a0-3780-4d5c-b9a7-f169994ae815'],['Week 2'],['Regular Season'],['Series 3'],['2021-01-29'],['CLMN']])
urls.append([['3f77eef0-6ea5-4d4e-9feb-3c8c6528b42b'],['Week 2'],['Regular Season'],['Series 3'],['2021-01-29'],['CLMN']])
urls.append([['e266f1f8-86c3-40bd-83d4-28b9d2c127fa'],['Week 2'],['Regular Season'],['Series 3'],['2021-01-29'],['CLMN']])
urls.append([['a4e5f41b-08d7-47c4-a254-17faad068e90'],['Week 2'],['Regular Season'],['Series 4'],['2021-01-29'],['CLMN']])
urls.append([['bdfa668a-eb0d-4ddc-8ee3-04f152d2dd19'],['Week 2'],['Regular Season'],['Series 4'],['2021-01-29'],['CLMN']])
urls.append([['14149ca9-4687-48ac-9bcd-18a92fe9df71'],['Week 2'],['Regular Season'],['Series 4'],['2021-01-29'],['CLMN']])
urls.append([['9701370c-565f-4ea3-9e67-c306e1ca1e54'],['Week 2'],['Regular Season'],['Series 4'],['2021-01-29'],['CLMN']])
urls.append([['38b3c6d1-6dad-4b50-942f-d12c8d49aa0f'],['Week 2'],['Regular Season'],['Series 5'],['2021-01-29'],['CLMN']])
urls.append([['4c344ba0-c2e8-4947-a0ce-d20857b06553'],['Week 2'],['Regular Season'],['Series 5'],['2021-01-29'],['CLMN']])
urls.append([['4e379a51-cbc6-4a41-950b-4a64846272a2'],['Week 2'],['Regular Season'],['Series 5'],['2021-01-29'],['CLMN']])
urls.append([['b4559c66-a375-4b35-b656-c72854870233'],['Week 2'],['Regular Season'],['Series 5'],['2021-01-29'],['CLMN']])

#2/5 CLMN Regular Season week 3
urls.append([['19620839-c4f1-4523-92bf-33c825b17fe5'],['Week 3'],['Regular Season'],['Series 1'],['2021-02-05'],['CLMN']])
urls.append([['264904a2-0746-4fa3-9461-7781aba52b1b'],['Week 3'],['Regular Season'],['Series 1'],['2021-02-05'],['CLMN']])
urls.append([['0c5512e0-cd7a-4e1c-ae01-49bc207e0c80'],['Week 3'],['Regular Season'],['Series 1'],['2021-02-05'],['CLMN']])
urls.append([['6dfffc80-018a-406e-bcdf-a48edb2b4fb4'],['Week 3'],['Regular Season'],['Series 1'],['2021-02-05'],['CLMN']])
urls.append([['29955940-910f-4cda-a304-b40353412746'],['Week 3'],['Regular Season'],['Series 2'],['2021-02-05'],['CLMN']])
urls.append([['ec91c503-f921-419b-9436-5de779d926d4'],['Week 3'],['Regular Season'],['Series 2'],['2021-02-05'],['CLMN']])
urls.append([['379689b6-ccf2-4243-94a8-e9d1cbae6a26'],['Week 3'],['Regular Season'],['Series 2'],['2021-02-05'],['CLMN']])

urls.append([['55a12399-151f-4194-b1f9-aa400add388f'],['Week 3'],['Regular Season'],['Series 3'],['2021-02-05'],['CLMN']])
urls.append([['71526d7c-f9c1-47ea-9d7f-e275124faee8'],['Week 3'],['Regular Season'],['Series 3'],['2021-02-05'],['CLMN']])
urls.append([['6f6269fd-e565-45d7-b386-319d6814c8d8'],['Week 3'],['Regular Season'],['Series 3'],['2021-02-05'],['CLMN']])
urls.append([['54641639-0c71-4c16-8994-123e9df39f16'],['Week 3'],['Regular Season'],['Series 3'],['2021-02-05'],['CLMN']])
urls.append([['fadb48fa-0b2b-48fc-85d9-b1f9f01e05f7'],['Week 3'],['Regular Season'],['Series 3'],['2021-02-05'],['CLMN']])
#series 4 was a forfeit
urls.append([['4b2991c4-0bd9-4901-a2e4-7becbe7be548'],['Week 3'],['Regular Season'],['Series 5'],['2021-02-05'],['CLMN']])
urls.append([['6fc27ba6-1a70-449a-8aee-81bb533cb543'],['Week 3'],['Regular Season'],['Series 5'],['2021-02-05'],['CLMN']])
urls.append([['9e5a0360-8ef6-4f8d-bcf6-6ece371d4487'],['Week 3'],['Regular Season'],['Series 5'],['2021-02-05'],['CLMN']])
urls.append([['d102c99d-90fe-4d00-abf3-4a5406ce5e44'],['Week 3'],['Regular Season'],['Series 5'],['2021-02-05'],['CLMN']])


#2/12 CLMN Regular Season week 4
#series 1 was a forfeit
urls.append([['f7c31af4-377d-4d0b-936f-8922dee193b9'],['Week 4'],['Regular Season'],['Series 2'],['2021-02-12'],['CLMN']])
urls.append([['752f900d-a5a9-4607-a14c-f670e0fe6eb0'],['Week 4'],['Regular Season'],['Series 2'],['2021-02-12'],['CLMN']])
urls.append([['4e9114fc-1fb0-4def-8b60-b6b19d8f7eed'],['Week 4'],['Regular Season'],['Series 2'],['2021-02-12'],['CLMN']])
urls.append([['f0dfa131-5e06-41fe-8d65-26efc4488792'],['Week 4'],['Regular Season'],['Series 3'],['2021-02-12'],['CLMN']])
urls.append([['150daf48-5dc4-4657-87b8-0b5f0a602839'],['Week 4'],['Regular Season'],['Series 3'],['2021-02-12'],['CLMN']])
urls.append([['ab83dd3a-13d1-4542-8662-d9fc13b1ea8e'],['Week 4'],['Regular Season'],['Series 3'],['2021-02-12'],['CLMN']])
urls.append([['790bae5d-b8cf-4f8c-b100-daa3f3a1f058'],['Week 4'],['Regular Season'],['Series 3'],['2021-02-12'],['CLMN']])
urls.append([['de7961b0-ef96-40f4-bccb-9ea155498c51'],['Week 4'],['Regular Season'],['Series 3'],['2021-02-12'],['CLMN']])
urls.append([['f4183f2b-933a-4519-bbb5-4a182a4e9ffe'],['Week 4'],['Regular Season'],['Series 4'],['2021-02-12'],['CLMN']])
urls.append([['d5cb15c7-604b-4d88-838f-847629dae52d'],['Week 4'],['Regular Season'],['Series 4'],['2021-02-12'],['CLMN']])
urls.append([['2770b15d-dfd3-4463-a76d-d4302b7dbeea'],['Week 4'],['Regular Season'],['Series 4'],['2021-02-12'],['CLMN']])
urls.append([['ffb16014-098e-4fc9-bd71-1b007f852a37'],['Week 4'],['Regular Season'],['Series 4'],['2021-02-12'],['CLMN']])
urls.append([['dcf250c7-e1f2-472c-b442-76b87928eb88'],['Week 4'],['Regular Season'],['Series 5'],['2021-02-12'],['CLMN']])
urls.append([['95f7f513-6a65-4ab9-9e43-ce6da831fb80'],['Week 4'],['Regular Season'],['Series 5'],['2021-02-12'],['CLMN']])
urls.append([['1a5a5c3d-444b-493e-a05e-b3c5c7b56914'],['Week 4'],['Regular Season'],['Series 5'],['2021-02-12'],['CLMN']])
urls.append([['10c3ab16-928d-4ff8-b0e0-2052699fa8b3'],['Week 4'],['Regular Season'],['Series 5'],['2021-02-12'],['CLMN']])
urls.append([['72f3c7cf-b762-4084-9fd3-9a776c5345ec'],['Week 4'],['Regular Season'],['Series 5'],['2021-02-12'],['CLMN']])


#2/12 bemidji scrim to warm up for their game
#need to fix null team names to add these games
#urls.append([['9f388b46-8600-4d0d-909a-1d60d6c01a3a'],['Week 0'],['Preseason'],['Series 11'],['2021-02-12']])
#urls.append([['97f84c47-767e-4277-8472-ef7bf2dd143a'],['Week 0'],['Preseason'],['Series 11'],['2021-02-12']])
#urls.append([['26372b1a-59bc-4f88-ae79-5138d3939220'],['Week 0'],['Preseason'],['Series 11'],['2021-02-12']])
#urls.append([['f67a2dad-c61b-4b3e-a529-e0b18adf0672'],['Week 0'],['Preseason'],['Series 11'],['2021-02-12']])
#urls.append([['82f84aa3-e981-489b-9e32-b0a6f3a5329c'],['Week 0'],['Preseason'],['Series 11'],['2021-02-12']])

#print(urls)

#initalize summary dataframes

for url in urls:
    #print(url)

    #download playerfile
    playerfile = 'C:/Users/mcdan/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/PLAYER_'+url[0][0]+'.csv'
    #playerfile = 'C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/PLAYER_'+url[0][0]+'.csv'
    fullplayerurl = 'https://ballchasing.com/dl/stats/players/'+url[0][0]+'/'+url[0][0]+'-players.csv'
    download_file(url=fullplayerurl,filename=playerfile)

    #find my row
    playerdata = pd.read_csv(playerfile, sep=';')
    
    #override player names for consistency
    playerinputs = [
         playerdata['player name'].str.upper() == "ZIM"
         ,playerdata['player name'].str.upper() == "DICEY #WE<3ZBRUH"
         ,playerdata['player name'].str.upper() == "TARR_RL DEMOS ONLY"
         ,playerdata['player name'].str.upper() == "M8ITSNATE"
         ,playerdata['player name'].str.upper() == "KING WASTEE"
         ,playerdata['player name'].str.upper() == "EL BLOOP :D"
         ,playerdata['player name'].str.upper() == "TIBBLE TOT"
         ,playerdata['player name'].str.upper() == "CZCHR."
         ,True
    ]
    playeroutputs = [
        "iChaotic"
        ,"Dicey"
        ,"Tarr_RL"
        ,'ItsNate'
        ,'RAPTOR Wastee'
        ,'El Bloop'
        ,'tibbles'
        ,'CzechR.'
        ,playerdata['player name']
    ]
    
    playerdata['player name'] = np.select(playerinputs,playeroutputs)
    #playerdata
    
    #add column that has guid for game
    playerdata['Game'] = url[0][0]
    
    #add column for season match type
    playerdata['Match Type'] = url[2][0]

    #add column for week number
    playerdata['Week Number'] = url[1][0]
    
    #add column for game date
    playerdata['Game Date'] = url[4][0]

    #add column for league
    playerdata['League'] = url[5][0]
    
    #write back to csv
    playerdata.to_csv(playerfile, sep=';', encoding='utf-8',index=False)


    #download team file
    teamfile = 'C:/Users/mcdan/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/TEAM_'+url[0][0]+'.csv'
    #teamfile = 'C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/TEAM_'+url[0][0]+'.csv'
    fullteamurl = 'https://ballchasing.com/dl/stats/teams/'+url[0][0]+'/'+url[0][0]+'-team-stats.csv'
    download_file(url=fullteamurl,filename=teamfile)

    teamdata = pd.read_csv(teamfile, sep=';')

    #add column to add team names for my team and opponents
    #teamdata['Team'] = np.where(teamdata['color'] != mycolor,'Opponent','Rochester Riff')


    #override team names for consistency
    teaminputs = [
         teamdata['team name'].str.upper() == "DULUTH", teamdata['team name'].str.upper() == 'SPIRIT'
        ,teamdata['team name'].str.upper() == "ROCHESTER", teamdata['team name'].str.upper() == 'RIFF'
        ,teamdata['team name'].str.upper() == "MINNETONKA", teamdata['team name'].str.upper() == 'BONZERS'
        ,teamdata['team name'].str.upper() == "HIBBING", teamdata['team name'].str.upper() == 'WARDENS'
        ,teamdata['team name'].str.upper() == "MINNEAPOLIS", teamdata['team name'].str.upper() == 'PRODIGIES'
        ,teamdata['team name'].str.upper() == "ST. CLOUD", teamdata['team name'].str.upper() == "ST CLOUD", teamdata['team name'].str.upper() == 'SOAR'
        ,teamdata['team name'].str.upper() == "ST. PAUL", teamdata['team name'].str.upper() == "ST PAUL", teamdata['team name'].str.upper() == 'KINGPINS'
        ,teamdata['team name'].str.upper() == "BLOOMINGTON", teamdata['team name'].str.upper() == 'URSAS', teamdata['team name'].str.upper() == 'BOOSTY BOYS' 
        ,teamdata['team name'].str.upper() == "BURNSVILLE", teamdata['team name'].str.upper() == 'FIRESTORM'
        ,teamdata['team name'].str.upper() == "BEMIDJI", teamdata['team name'].str.upper() == 'BEAVERS'
        ,True
    ]
    teamoutputs = [
        "DULUTH","DULUTH"
        ,"ROCHESTER","ROCHESTER"
        ,"MINNETONKA","MINNETONKA"
        ,"HIBBING","HIBBING"
        ,"MINNEAPOLIS","MINNEAPOLIS"
        ,"ST. CLOUD","ST. CLOUD","ST. CLOUD"
        ,"ST. PAUL","ST. PAUL","ST. PAUL"
        ,"BLOOMINGTON","BLOOMINGTON","BLOOMINGTON"
        ,"BURNSVILLE","BURNSVILLE"
        ,"BEMIDJI","BEMIDJI"
        ,teamdata['team name']
    ]
    
    teamdata['team name'] = np.select(teaminputs,teamoutputs)
    #teamdata

    #add column that has guid for game
    teamdata['Game'] = url[0][0]

    #add column for season match type
    teamdata['Match Type'] = url[2][0]

    #add column for week number
    teamdata['Week Number'] = url[1][0]

    #add column for game date
    teamdata['Game Date'] = url[4][0]

    #add column for league
    teamdata['League'] = url[5][0]

    #add column for week number
    teamdata['Series Number'] = url[3][0]
    #teamdata

    #compare goals by each team to calculate winning team
    bluegoals = teamdata[teamdata['color'] == 'blue']
    bluegoals = bluegoals['goals'].values[0]

    orangegoals = teamdata[teamdata['color'] == 'orange']
    orangegoals = orangegoals['goals'].values[0]

    #compare the two values to calculate winning team
    if bluegoals > orangegoals:
        winner = 'blue'
    else:
        winner = 'orange'
    #print(winner)

    #set result column using winner from above
    teamdata['Result'] = ''
    teamdata.loc[teamdata['color'] == winner, 'Result'] = 'Win'
    teamdata.loc[teamdata['color'] != winner, 'Result'] = 'Loss'
    #teamdata

    #write back to csv
    teamdata.to_csv(teamfile, sep=';', encoding='utf-8',index=False)