 function rate(star) {
            const stars = document.querySelectorAll('.star');
            stars.forEach((s, index) => {
                if (index < star) {
                    s.classList.add('active');
                } else {
                    s.classList.remove('active');
                }
            });
           
        }


        function enterFeedback() {
            alert('Enter button clicked!');
            document.querySelector('textarea[placeholder="Your comments here..."]').focus();

        }

        function submitFeedback() {
            alert('Feedback submitted!');
        }