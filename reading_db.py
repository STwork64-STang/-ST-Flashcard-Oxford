# reading_db.py
# รวมเรื่องสั้นจาก Kru Whan พร้อมคำถาม Multiple Choice (ถามความเข้าใจเนื้อเรื่อง)

STORIES = [
    {
        "id": 1,
        "title": "Samantha and Maria",
        "level": "A1-B1",
        "topic": "Friendship & Sports",
        "emoji": "🏀",
        "text": (
            "Samantha is a young girl who loves playing basketball. Every day after school, "
            "she goes to the park with her friends to play basketball. One day, she noticed a "
            "new girl watching them play. Samantha introduced herself and asked if she wanted "
            "to join in. The new girl, Maria, was shy at first but soon started to enjoy the "
            "game. After they finished playing, Samantha asked Maria if she wanted to come "
            "back and play with them again tomorrow. Maria smiled and said yes. From that day "
            "on, Maria became a regular player with Samantha and her friends, and they all "
            "had a great time playing basketball together."
        ),
        "thai": (
            "ซแมนตาเป็นเด็กสาวที่ชอบเล่นบาสเก็ตบอลมาก ทุกวันหลังจากเลิกเรียน เธอมักไปเล่นที่สวน"
            "สาธารณะกับเพื่อนๆ ของเธอ วันหนึ่งเธอสังเกตเห็นเด็กผู้หญิงคนหนึ่งกำลังดูพวกเธอเล่นบาสเก็ตบอล"
            " ซแมนตาจึงแนะนำตัวเองและถามเด็กสาวคนนั้นว่าอยากเล่นด้วยกันไหม เด็กสาวคนนั้นชื่อมาเรีย"
            " เธอเขินอายในช่วงแรก แต่พอเล่นไปเรื่อยๆ เธอก็เริ่มจะสนุกกับมัน"
        ),
        "questions": [
            {
                "q": "Where does Samantha go after school every day?",
                "options": [
                    "A) To the library",
                    "B) To the park",
                    "C) To her friend's house",
                    "D) To a basketball court"
                ],
                "answer": "B) To the park",
                "explanation": "The story says 'she goes to the park with her friends to play basketball.'"
            },
            {
                "q": "How did Maria feel when she first joined the game?",
                "options": [
                    "A) Excited and confident",
                    "B) Angry and upset",
                    "C) Shy at first",
                    "D) Bored and tired"
                ],
                "answer": "C) Shy at first",
                "explanation": "The story says 'Maria, was shy at first but soon started to enjoy the game.'"
            },
            {
                "q": "What happened to Maria after that day?",
                "options": [
                    "A) She moved to a different school",
                    "B) She stopped playing basketball",
                    "C) She became a regular player with the group",
                    "D) She won a basketball championship"
                ],
                "answer": "C) She became a regular player with the group",
                "explanation": "The story says 'Maria became a regular player with Samantha and her friends.'"
            },
            {
                "q": "What is the main message of this story?",
                "options": [
                    "A) Basketball is the best sport",
                    "B) Being kind and welcoming can create new friendships",
                    "C) Shy people should stay home",
                    "D) You should only play with people you know"
                ],
                "answer": "B) Being kind and welcoming can create new friendships",
                "explanation": "Samantha welcomed Maria, and this kindness led to a new friendship."
            },
        ]
    },
    {
        "id": 2,
        "title": "Lena and the Injured Bird",
        "level": "A1-B1",
        "topic": "Kindness & Nature",
        "emoji": "🐦",
        "text": (
            "Lena is a young girl who loves animals. One day, she found a small bird with a "
            "broken wing on the ground. Lena felt sad for the bird and wanted to help. She "
            "took the bird home and made a small nest for it. Lena cared for the bird every "
            "day, feeding it and ensuring it was comfortable. After a few weeks, the bird's "
            "wing had healed and was ready to fly again. Lena was happy to see the bird fly "
            "away but felt a little sad to say goodbye to her feathered friend. However, Lena "
            "knew that she had helped the bird when it needed her most."
        ),
        "thai": (
            "ลีนาเป็นเด็กสาวที่รักสัตว์มากๆ วันหนึ่งเธอพบกับนกตัวน้อยที่ปีกได้รับบาดเจ็บบนพื้น "
            "ลีนารู้สึกแย่มากและอยากจะช่วยเหลือมัน เธอพานกตัวนั้นกลับบ้านและทำรังเล็กๆ ให้มัน "
            "ลีนาดูแลนกตัวนั้นทุกวัน ให้อาหารมันและทำให้มันสบายที่สุด หลังจากนั้นไม่กี่สัปดาห์ "
            "ปีกของนกตัวนั้นหายดีและกลับมาบินได้อีกครั้ง"
        ),
        "questions": [
            {
                "q": "What problem did the bird have when Lena found it?",
                "options": [
                    "A) It was lost",
                    "B) It had a broken wing",
                    "C) It was hungry",
                    "D) It had no feathers"
                ],
                "answer": "B) It had a broken wing",
                "explanation": "The story says 'she found a small bird with a broken wing on the ground.'"
            },
            {
                "q": "What did Lena do to help the bird?",
                "options": [
                    "A) She called a vet",
                    "B) She left it in the park",
                    "C) She took it home and made a nest for it",
                    "D) She put it in a cage"
                ],
                "answer": "C) She took it home and made a nest for it",
                "explanation": "The story says 'She took the bird home and made a small nest for it.'"
            },
            {
                "q": "How did Lena feel when the bird flew away?",
                "options": [
                    "A) Only happy",
                    "B) Only sad",
                    "C) Happy but also a little sad",
                    "D) Angry and upset"
                ],
                "answer": "C) Happy but also a little sad",
                "explanation": "The story says 'Lena was happy to see the bird fly away but felt a little sad.'"
            },
            {
                "q": "What does this story teach us?",
                "options": [
                    "A) Wild birds should be kept as pets",
                    "B) We should help others who are in need",
                    "C) It is dangerous to touch birds",
                    "D) Birds can't recover from injuries"
                ],
                "answer": "B) We should help others who are in need",
                "explanation": "Lena helped the bird when it needed her most, showing the importance of caring for others."
            },
        ]
    },
    {
        "id": 3,
        "title": "Tom's Kind Gesture",
        "level": "A1-B1",
        "topic": "Kindness & Community",
        "emoji": "⚽",
        "text": (
            "Tom is a young boy who loves to play soccer. He and his friends were playing "
            "soccer in the park when a sudden rainstorm started. They ran to a nearby shelter "
            "to wait for the rain to stop. While they were waiting, they noticed an old man "
            "sitting on a bench looking wet and cold. Tom felt sorry for the man and decided "
            "to give him his jacket. The old man was grateful for the kind gesture and thanked "
            "Tom. The rain eventually stopped, and Tom and his friends continued playing "
            "soccer. But Tom felt happy knowing that he had helped someone who needed it."
        ),
        "thai": (
            "ทอมเป็นเด็กหนุ่มที่ชอบเล่นฟุตบอลมาก ขณะที่เขาและเพื่อนๆ ของเขากำลังเล่นฟุตบอลที่สวน"
            "สาธารณะ จู่ๆ พายุฝนก็โหมกระหน่ำ พวกเขาวิ่งไปที่กำบังใกล้ๆ เพื่อรอให้ฝนหยุดตก "
            "ขณะที่พวกเขากำลังรออยู่นั้น พวกเขาสังเกตเห็นชายชราที่ทั้งเปียกและดูหนาวสั่นนั่งอยู่ที่ม้านั่ง"
        ),
        "questions": [
            {
                "q": "Why did Tom and his friends run to a shelter?",
                "options": [
                    "A) They were tired of playing",
                    "B) A rainstorm started suddenly",
                    "C) They were looking for food",
                    "D) Their parents called them"
                ],
                "answer": "B) A rainstorm started suddenly",
                "explanation": "The story says 'when a sudden rainstorm started.'"
            },
            {
                "q": "What did Tom notice at the shelter?",
                "options": [
                    "A) A stray dog",
                    "B) His lost ball",
                    "C) An old man who was wet and cold",
                    "D) A broken bench"
                ],
                "answer": "C) An old man who was wet and cold",
                "explanation": "The story says 'they noticed an old man sitting on a bench looking wet and cold.'"
            },
            {
                "q": "What did Tom do to help the old man?",
                "options": [
                    "A) He shared his food",
                    "B) He gave the man his jacket",
                    "C) He called for help",
                    "D) He found an umbrella"
                ],
                "answer": "B) He gave the man his jacket",
                "explanation": "The story says 'Tom felt sorry for the man and decided to give him his jacket.'"
            },
            {
                "q": "How did Tom feel after helping the old man?",
                "options": [
                    "A) Cold and unhappy",
                    "B) Proud and happy",
                    "C) Tired and bored",
                    "D) Nervous and scared"
                ],
                "answer": "B) Proud and happy",
                "explanation": "The story says 'Tom felt happy knowing that he had helped someone who needed it.'"
            },
        ]
    },
    {
        "id": 4,
        "title": "Princess Lily's Journey",
        "level": "A1-B1",
        "topic": "Fairy Tale & Bravery",
        "emoji": "👸",
        "text": (
            "Once upon a time, there was a kind-hearted princess named Lily. She lived in a "
            "big castle with her parents, the king and queen. One day, a wicked witch put a "
            "curse on the castle, and everyone in it fell into a deep sleep. The princess went "
            "on a journey to find the witch and asked her to remove the curse. Along the way, "
            "she met a talking horse who became her friend and guide. After many adventures, "
            "the princess found the witch and convinced her to remove the curse. Everyone in "
            "the castle woke up, and the princess and the horse lived happily ever after."
        ),
        "thai": (
            "กาลครั้งหนึ่งนานมาแล้ว มีเจ้าหญิงผู้เปี่ยมไปด้วยจิตใจที่มีความเมตตากรุณาอยู่องค์หนึ่ง "
            "เธอมีนามว่าลิลลี่ เจ้าหญิงอาศัยอยู่ในปราสาทหลังใหญ่กับพ่อแม่ของเธอ นั่นก็คือพระราชา"
            "และพระราชินี วันหนึ่งนางแม่มดชั่วร้ายสาปให้ทุกคนในปราสาทให้ตกอยู่ในนิทรา"
        ),
        "questions": [
            {
                "q": "What happened to the people in the castle?",
                "options": [
                    "A) They escaped from the castle",
                    "B) They fell into a deep sleep because of a curse",
                    "C) They went on a journey",
                    "D) They fought against the witch"
                ],
                "answer": "B) They fell into a deep sleep because of a curse",
                "explanation": "The story says 'a wicked witch put a curse on the castle, and everyone in it fell into a deep sleep.'"
            },
            {
                "q": "Who helped Princess Lily on her journey?",
                "options": [
                    "A) The king and queen",
                    "B) A dragon",
                    "C) A talking horse",
                    "D) The witch's assistant"
                ],
                "answer": "C) A talking horse",
                "explanation": "The story says 'she met a talking horse who became her friend and guide.'"
            },
            {
                "q": "How did Princess Lily solve the problem?",
                "options": [
                    "A) She fought the witch with magic",
                    "B) She convinced the witch to remove the curse",
                    "C) She found a magic potion",
                    "D) She asked the king to help"
                ],
                "answer": "B) She convinced the witch to remove the curse",
                "explanation": "The story says 'the princess found the witch and convinced her to remove the curse.'"
            },
            {
                "q": "What quality does Princess Lily show in this story?",
                "options": [
                    "A) Laziness and fear",
                    "B) Bravery and determination",
                    "C) Cruelty and selfishness",
                    "D) Shyness and weakness"
                ],
                "answer": "B) Bravery and determination",
                "explanation": "Princess Lily went on a dangerous journey alone to save her people, showing great bravery."
            },
        ]
    },
    {
        "id": 5,
        "title": "The Ant and the Grasshopper",
        "level": "A1-B1",
        "topic": "Fable & Hard Work",
        "emoji": "🐜",
        "text": (
            "Once upon a time, there was a hardworking ant who spent all summer gathering "
            "food for the winter. The ant knew that winter would be tough and wanted to be "
            "prepared. Meanwhile, a lazy grasshopper spent all summer playing and having fun. "
            "When winter arrived, the ant had plenty of food to eat, but the grasshopper had "
            "nothing. The grasshopper asked the ant for help, but the ant refused. The "
            "grasshopper realized that he should have been more like the ant and worked hard "
            "to prepare for the winter."
        ),
        "thai": (
            "กาลครั้งหนึ่งนานมาแล้ว มีเจ้ามดจอมขยันอยู่ตัวหนึ่ง มันใช้เวลาตลอดทั้งฤดูร้อนรวบรวม"
            "อาหารไว้สำหรับตอนฤดูหนาว เจ้ามดรู้ดีว่ามันยากลำบากแค่ไหนในฤดูหนาวเลยอยากจะ"
            "เตรียมตัวไว้ก่อน ในระหว่างนั้นเจ้าตั๊กแตนจอมขี้เกียจใช้เวลาตลอดทั้งฤดูร้อนเที่ยวเล่น"
            "สนุกสนาน"
        ),
        "questions": [
            {
                "q": "What did the ant do all summer?",
                "options": [
                    "A) Played and had fun",
                    "B) Slept all day",
                    "C) Gathered food for winter",
                    "D) Traveled to new places"
                ],
                "answer": "C) Gathered food for winter",
                "explanation": "The story says 'a hardworking ant who spent all summer gathering food for the winter.'"
            },
            {
                "q": "What happened to the grasshopper when winter came?",
                "options": [
                    "A) He had plenty of food",
                    "B) He had nothing to eat",
                    "C) He found food in the forest",
                    "D) He moved to a warm place"
                ],
                "answer": "B) He had nothing to eat",
                "explanation": "The story says 'the grasshopper had nothing.'"
            },
            {
                "q": "What did the grasshopper learn from this experience?",
                "options": [
                    "A) Ants are selfish creatures",
                    "B) Winter is not that bad",
                    "C) He should have worked hard to prepare like the ant",
                    "D) Playing is more important than working"
                ],
                "answer": "C) He should have worked hard to prepare like the ant",
                "explanation": "The story says 'The grasshopper realized that he should have been more like the ant and worked hard.'"
            },
            {
                "q": "What is the moral (บทเรียน) of this story?",
                "options": [
                    "A) Always help your friends",
                    "B) Hard work and preparation pay off",
                    "C) Never share your food",
                    "D) Summer is the best season"
                ],
                "answer": "B) Hard work and preparation pay off",
                "explanation": "The ant prepared well and survived winter, while the lazy grasshopper suffered."
            },
        ]
    },
    {
        "id": 6,
        "title": "Sophie's Dance",
        "level": "A1-B1",
        "topic": "Courage & Self-belief",
        "emoji": "💃",
        "text": (
            "Sophie was a shy girl who loved to dance. She dreamed of performing on stage but "
            "was too nervous to audition for the school talent show. With encouragement from "
            "her best friend, Sophie finally built up the courage to try out. Despite her "
            "nerves, Sophie danced beautifully and was chosen to perform at the show. When the "
            "day came, Sophie took a deep breath and stepped onto the stage. As she began to "
            "dance, her nerves melted away, and she felt free and confident. From that day "
            "forward, Sophie continued to pursue her passion for dance, unafraid of taking "
            "risks and stepping out of her comfort zone."
        ),
        "thai": (
            "โซฟีเป็นเด็กสาวขี้อายผู้หลงใหลในการเต้นรำ เธอฝันอยากจะแสดงบนเวทีสักครั้งแต่ก็กังวล"
            "เกินกว่าจะไปคัดตัวสำหรับงานแสดงความสามารถของโรงเรียน แต่ด้วยการสนับสนุนของ"
            "เพื่อนสนิทของโซฟี เธอก็ได้รวบรวมความกล้าและลองทำมัน"
        ),
        "questions": [
            {
                "q": "Why didn't Sophie audition for the talent show at first?",
                "options": [
                    "A) She didn't like dancing",
                    "B) She was too nervous",
                    "C) She wasn't allowed to",
                    "D) She didn't know about it"
                ],
                "answer": "B) She was too nervous",
                "explanation": "The story says 'she dreamed of performing on stage but was too nervous to audition.'"
            },
            {
                "q": "Who helped Sophie find the courage to try out?",
                "options": [
                    "A) Her teacher",
                    "B) Her parents",
                    "C) Her best friend",
                    "D) A famous dancer"
                ],
                "answer": "C) Her best friend",
                "explanation": "The story says 'With encouragement from her best friend, Sophie finally built up the courage to try out.'"
            },
            {
                "q": "What happened to Sophie's nerves when she started dancing on stage?",
                "options": [
                    "A) They got worse",
                    "B) She ran off the stage",
                    "C) They melted away and she felt confident",
                    "D) She forgot her routine"
                ],
                "answer": "C) They melted away and she felt confident",
                "explanation": "The story says 'her nerves melted away, and she felt free and confident.'"
            },
            {
                "q": "What did Sophie learn from this experience?",
                "options": [
                    "A) Dancing is too difficult",
                    "B) She should always stay in her comfort zone",
                    "C) Taking risks and believing in yourself leads to growth",
                    "D) Talent shows are not worth it"
                ],
                "answer": "C) Taking risks and believing in yourself leads to growth",
                "explanation": "Sophie learned to be 'unafraid of taking risks and stepping out of her comfort zone.'"
            },
        ]
    },
    {
        "id": 7,
        "title": "Max's Comeback",
        "level": "A1-B1",
        "topic": "Perseverance & Teamwork",
        "emoji": "🏆",
        "text": (
            "Max loved to play soccer and was his school's team captain. One day, during a "
            "big game, Max injured his ankle and could not play for the rest of the season. "
            "He felt disappointed and frustrated, but he didn't give up. Instead, he cheered "
            "on his teammates and helped them practice whenever possible. Max also started "
            "working on his fitness, hoping to return stronger and better than ever. When the "
            "next season rolled around, Max was back on the field, leading his team to "
            "victory. He learned that setbacks are just temporary and that with determination "
            "and hard work, anything is possible."
        ),
        "thai": (
            "แม็กซ์ชอบเล่นฟุตบอลมาก และเขาก็เป็นหัวหน้าทีมฟุตบอลของโรงเรียน วันหนึ่งระหว่าง"
            "การแข่งขัน แม็กซ์ได้รับบาดเจ็บที่ข้อเท้าจนทำให้เขาไม่สามารถลงเล่นเกมที่เหลือในฤดูกาล"
            "ได้ เขารู้สึกสิ้นหวังและหงุดหงิดมากแต่เขาก็ไม่เคยยอมแพ้"
        ),
        "questions": [
            {
                "q": "What problem did Max face during the big game?",
                "options": [
                    "A) His team lost badly",
                    "B) He forgot how to play",
                    "C) He injured his ankle",
                    "D) He was removed from the team"
                ],
                "answer": "C) He injured his ankle",
                "explanation": "The story says 'Max injured his ankle and could not play for the rest of the season.'"
            },
            {
                "q": "What did Max do while he was injured?",
                "options": [
                    "A) He quit the team",
                    "B) He cheered teammates and worked on his fitness",
                    "C) He watched TV all day",
                    "D) He switched to a different sport"
                ],
                "answer": "B) He cheered teammates and worked on his fitness",
                "explanation": "The story says he 'cheered on his teammates' and 'started working on his fitness.'"
            },
            {
                "q": "What happened when the next season came?",
                "options": [
                    "A) Max was still injured",
                    "B) Max retired from soccer",
                    "C) Max returned and led his team to victory",
                    "D) Max moved to a new school"
                ],
                "answer": "C) Max returned and led his team to victory",
                "explanation": "The story says 'Max was back on the field, leading his team to victory.'"
            },
            {
                "q": "What important lesson did Max learn?",
                "options": [
                    "A) Soccer is too dangerous to play",
                    "B) Setbacks are permanent and life is unfair",
                    "C) Setbacks are temporary; determination and hard work make anything possible",
                    "D) Captains should never play in big games"
                ],
                "answer": "C) Setbacks are temporary; determination and hard work make anything possible",
                "explanation": "The story says 'He learned that setbacks are just temporary and that with determination and hard work, anything is possible.'"
            },
        ]
    },
    {
        "id": 8,
        "title": "Amy's Dream",
        "level": "A1-B1",
        "topic": "Self-belief & Perseverance",
        "emoji": "🎤",
        "text": (
            "Amy was a young girl who loved to sing. She would sing everywhere she went, in "
            "the shower, on the bus, and even in class. Her classmates would often tease her, "
            "telling her to be quiet. But Amy didn't let their comments bring her down. She "
            "continued to sing every day, believing in herself and her talent. One day, a "
            "music producer heard Amy singing and offered her a record deal. Amy's dreams had "
            "come true, all because she believed in herself and never gave up."
        ),
        "thai": (
            "เอมีเป็นเด็กสาวผู้ชื่นชอบการร้องเพลง เธอจะร้องเพลงในทุกที่ที่เธอไป ในห้องอาบน้ำ บน"
            "รถบัส หรือแม้กระทั่งในห้องเรียน เพื่อนร่วมห้องของเอมีจะชอบแกล้งเธอโดยการบอกให้เธอ"
            "เงียบซะ แต่เอมีไม่ปล่อยให้คำวิจารณ์เหล่านั้นทำให้ตัวเองรู้สึกแย่"
        ),
        "questions": [
            {
                "q": "How did Amy's classmates react to her singing?",
                "options": [
                    "A) They encouraged her",
                    "B) They joined in with her",
                    "C) They often teased her and told her to be quiet",
                    "D) They ignored her"
                ],
                "answer": "C) They often teased her and told her to be quiet",
                "explanation": "The story says 'Her classmates would often tease her, telling her to be quiet.'"
            },
            {
                "q": "What did Amy do when her classmates teased her?",
                "options": [
                    "A) She stopped singing",
                    "B) She cried and stayed home",
                    "C) She continued to sing every day",
                    "D) She argued with them"
                ],
                "answer": "C) She continued to sing every day",
                "explanation": "The story says 'She continued to sing every day, believing in herself and her talent.'"
            },
            {
                "q": "How did Amy's dream come true?",
                "options": [
                    "A) She won a singing competition",
                    "B) A music producer heard her and offered a record deal",
                    "C) Her teacher recommended her to a music school",
                    "D) She posted videos online"
                ],
                "answer": "B) A music producer heard her and offered a record deal",
                "explanation": "The story says 'a music producer heard Amy singing and offered her a record deal.'"
            },
            {
                "q": "What is the key message of Amy's story?",
                "options": [
                    "A) You need others to believe in you to succeed",
                    "B) Singing in class is a good idea",
                    "C) Believing in yourself and never giving up leads to success",
                    "D) Music producers are everywhere"
                ],
                "answer": "C) Believing in yourself and never giving up leads to success",
                "explanation": "Amy succeeded 'because she believed in herself and never gave up.'"
            },
        ]
    },
]
