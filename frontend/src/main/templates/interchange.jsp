<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Age Redirect Page</title>
</head>
<body>
    <script>
        fetch('./client_info.txt') 
            .then(response => response.text())
            .then(data => {
                const [client_age] = data.split('\n');

                if (client_age === 'normal') {
                    window.location.replace('./normalquestion.html');
                } else if (client_age === 'senior') {
                    window.location.replace('./grandquestion.html');
                }
            })
            .catch(error => {
                console.error('클라이언트 정보 오류 : ', error);
            });
    </script>
</body>
</html>