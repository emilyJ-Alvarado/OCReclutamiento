(function () {
    
    var questions = [{
        question: "AIESEC es una organización que requiere de personas capaces de superar dificultades... <br>Indique su nivel de persistencia.",
        choices: ["Alto", "Medio", "Bajo"]
    }, {        
        question: "Califique su nivel de liderazgo",
        choices: ["Alto", "Medio", "Bajo"]
    }, {
        question: "¿Es de su agrado compartir tus experiencias, momentos, valores?...  <br>¿Cómo califica su nivel de socialización?",
        choices: ["Alto", "Medio", "Bajo"]
    }, {
        question: "AIESEC te ayudará a desarrollar tus capacidades personales y profesionales. <br>¿Cuál es su expectativa al respecto?",
        choices: ["Alto", "Medio", "Bajo"]
    }, {
        question: "¿Qué tan importante es para usted defender causas sociales?",
        choices: ["Alto", "Medio", "Bajo"]
    }, {
        question: "¿Qué capacidad tienes para sorportar la presión social y de grupo?",
        choices: ["Alto", "Medio", "Bajo" ]
    }, {
        question: "¿Cuál es tu capacidad para solucionar problemas en corto tiempo?",
        choices: ["Alto", "Medio", "Bajo"]
    }, {
        question: "¿Con qué frecuencia terminas completamente tus tareas pendientes según lo has planificado?",
        choices: ["Alto", "Medio", "Bajo"]
    }, {
        question: 'AIESEC requiere mayormente de trabajo presencial, antes de virtual y mínimamente de 6 horas a la semana... <br>¿Cuál es su disponibilidad de tiempo?',
        choices: ["Alto", "Medio", "Bajo"]
    }, {
        question: "En AIESEC estamos muy motivados por las metas y trabajamos con programas estadísticos y análisis de datos para guiar nuestros resultados... <br>¿Cuál es tu nivel de uso de estas herramientas?",
        choices: ["Alto", "Medio", "Bajo"]
    } 
        
    ];


    var questionCounter = 0; //Tracks question number
    var selections = []; //Array containing user choices
    var quiz = $('#quiz'); //Quiz div object
    
    // Display initial question
    displayNext();

    // Click handler for the 'next' button
    $('#next').on('click', function (e) {
        e.preventDefault();

        // Suspend click listener during fade animation
        if (quiz.is(':animated')) {
            return false;
        }
        choose();

        // If no user selection, progress is stopped
        if (isNaN(selections[questionCounter])) {
            swal({
              title: "Información",
              text: "Debes marcar una opción.",
              icon: "info",
            });
        } else {
            questionCounter++;
            displayNext();
        }
    });

    // Click handler for the 'prev' button
    $('#prev').on('click', function (e) {
        e.preventDefault();

        if (quiz.is(':animated')) {
            return false;
        }
        choose();
        questionCounter--;
        displayNext();
    });


    $('#start').on('click', function (e) {
        e.preventDefault();

        if (quiz.is(':animated')) {
            return false;
        }
        questionCounter = 0;
        selections = [];
        $('#title.card-header').html("Selecciona la mejor respuesta según observes ...se totalmente sincero y objetivo(a).");
        $('#recomiendaPreTest').hide();
        displayNext();
        $('#start').hide();
    });


    $('#guardar').on('click', function (e) {
        e.preventDefault();
        if (quiz.is(':animated')) {
            return false;
        }
        $('#recomiendaPreTest').hide();
        //$('#start').hide();
        $('#guardar').hide();
    
      var id_usuario = $('#postulante-id').data("name");
      //alert(id_usuario);
      $.getJSON($SCRIPT_ROOT + '/post_diagnostico/'+id_usuario, {
        selections: JSON.stringify(selections)
      }, function(data) {
            var score = $('<p>', {id: 'question'});
            score.append(data.result);
            quiz.html(score).fadeIn();                   
      });           
        
        swal({
          title: "¡Excelente!",
          text: "Datos guardados correctamente",
          icon: "success",
        });   
        //url=$SCRIPT_ROOT + '/pythonlogin/home'  
        //setTimeout(function(){window.location = url;}, 2000);     
    });



    // Animates buttons on hover
    $('.button').on('mouseenter', function () {
        $(this).addClass('active');
    });
    $('.button').on('mouseleave', function () {
        $(this).removeClass('active');
    });


    // Creates and returns the div that contains the questions and
    // the answer selections
    function createQuestionElement(index) {
        var qElement = $('<div>', {
            id: 'question'
        });

        var header = $('<h2>Pregunta ' + (index + 1) + ':</h2>');
        qElement.append(header);
        //console.log (questions[index].question)
        
///////////////////////////////////////////////////////////////////////////////////////////////        
        
        /*
        if ((index + 1)==1 || (index + 1)==11 || (index + 1)==16){
            var segundos = 10;        
            var contador = setInterval(function() {           
                segundos--;          
                $("#contador-"+ (index + 1)).text(segundos+ " segundos");
                if (segundos <= 0) 
                    clearInterval(contador);
            }, 1000);        
                  
            
            setTimeout(function() {
              document.getElementById('image-'+ (index + 1)).style.display='none';   
              $("#contador-"+ (index + 1)).hide();                  
            }, 10*1000);
            
        }
        */
///////////////////////////////////////////////////////////////////////////////////////////////         
        
        var question = $('<p>').append(questions[index].question);
        qElement.append(question);

        var radioButtons = createRadios(index);
        qElement.append(radioButtons);

        return qElement;
    }

    // Creates a list of the answer choices as radio inputs
    function createRadios(index) {
        var radioList = $('<ul>');
        var item;
        var input = '';
        for (var i = 0; i < questions[index].choices.length; i++) {
            item = $('<li>');
            input = '<input type="radio" name="answer" value=' + i + ' />';
            input += ' ' + questions[index].choices[i];
            item.append(input);
            radioList.append(item);
        }
        return radioList;
    }

    // Reads the user selection and pushes the value to an array
    function choose() {
        selections[questionCounter] = +$('input[name="answer"]:checked').val();
    }

    // Displays next requested element
    function displayNext() {
        //var postulante_id = $('#postulante-id').data("name");
        //alert(postulante_id);
        quiz.fadeOut(function () {
            $('#question').remove();

            if (questionCounter < questions.length) {
                var nextQuestion = createQuestionElement(questionCounter);
                quiz.append(nextQuestion).fadeIn();
                if (!(isNaN(selections[questionCounter]))) {
                    $('input[value=' + selections[questionCounter] + ']').prop('checked', true);
                }

                // Controls display of 'prev' button
                if (questionCounter === 1) {
                    $('#prev').show();
                } else if (questionCounter === 0) {

                    $('#prev').hide();
                    $('#next').show();
                }
            } else {
            
                var scoreElem = displayScore();
                quiz.append(scoreElem).fadeIn();
                $('#next').hide();
                $('#prev').hide();
                //$('#start').show();
                $('#guardar').show();                
                $('#recomiendaPreTest').show();
            }
        });
    }

    // Computes score and returns a paragraph element to be displayed
    function displayScore() {
        $('#title.card-header').html("Resultados obtenidos:");
        var score = $('<p>', {id: 'question'});
        score.append('De click en "Guardar" para ver el resultado de la entrevista.');         
        
        return score;
    }
})();
