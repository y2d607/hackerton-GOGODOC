let currentQuestion = 1;
const totalQuestions = 6;

function showNextQuestion() {
    // 현재 질문의 라디오 버튼 체크 여부 확인
    const radios = document.querySelectorAll('#question' + currentQuestion + ' input[type="radio"]');
    const isAnswered = Array.from(radios).some(radio => radio.checked);

    if (!isAnswered) {
        alert('버튼을 체크해주세요.');
        return; // 답변이 체크되지 않았으므로 함수 종료
    }

    // 현재 질문 숨기기
    let currentDiv = document.getElementById('question' + currentQuestion);
    currentDiv.style.display = 'none';

    // 다음 질문 표시 또는 폼 제출
    currentQuestion++;
    if (currentQuestion <= totalQuestions) {
        let nextDiv = document.getElementById('question' + currentQuestion);
        nextDiv.style.display = 'block';
    } else {
        // 마지막 질문 후 이동할 페이지
        window.location.href = 'grandquestion_result.html';
    }
}