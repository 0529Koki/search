let currentQuestion = 1;  // 現在の質問の番号

document.getElementById('next-btn').addEventListener('click', function() {
    if (currentQuestion === 1) {
        // 質問1: 何人分か選んだ後
        let numPeople = document.querySelector('input[name="num_people"]:checked');
        if (numPeople) {
            document.getElementById('question1').style.display = 'none';  // 質問1を非表示
            document.getElementById('meal_type_container').style.display = 'block';  // 質問2を表示
            currentQuestion = 2;
        } else {
            alert("何人分か選んでください！");
        }
    } else if (currentQuestion === 2) {
        // 質問2: 食べたいジャンル選択後
        document.getElementById('meal_type_container').style.display = 'none';
        document.getElementById('ingredients_container').style.display = 'block';
        currentQuestion = 3;
    } else if (currentQuestion === 3) {
        // 質問3: 食材選択後
        document.getElementById('ingredients_container').style.display = 'none';
        document.getElementById('cooking_method_container').style.display = 'block';
        currentQuestion = 4;
    } else if (currentQuestion === 4) {
        // 質問4: 調理方法選択後
        // 最後の質問が終わったら検索を送信
        document.querySelector('form').submit();
    }
});
