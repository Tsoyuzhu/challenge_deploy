$(document).ready(function() {
    let file = null

    $('#predictionBtn').click(function() {
        let name = $('#predictionInput').val()
    
        // Check that all characters in the string are letters
        if (/^[a-zA-Z]+$/.test(name) && name.length > 0) {
            $.ajax({method: 'POST', url: $SCRIPT_ROOT+'/api/predict', data: JSON.stringify({name: name}), contentType: 'application/JSON', success: function(data, status) {
                $('#predictionResult').text(data.result)
            }})
        } else {
            $('#predictionResult').text('Error: Invalid name detected')
        }
    })

    $('#file-upload').change(function(event) {
        file = event.target.files[0]
        $('#uploadedFile').text(file.name)
    })
    
    $('#submitFile').click(function() {
        let data = new FormData()
        // Used for console messages
        date = new Date()
        if (file === null) {
            // Check if file is valid
            $('#console').append(`<p>${date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds()} You must upload a file first!</p>`)
        } else {
            // Read the file
            let reader = new FileReader();
            reader.readAsText(file);
            reader.onload = function(event) {
                var csvData = event.target.result;
                data = $.csv.toArrays(csvData);
                if (!(data && data.length > 0)) {
                    $('#console').append(`<p>${date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds()} Error loading training data: Your csv is empty or was not uploaded correctly.</p>`)
                } else {
                    $('#console').append(`<p>${date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds()} Imported -' + data.length + '- rows successfully!</p>`)
                    // Now verify the data
                    let result = verifyDataset(data)
                    if (!result.valid) {
                        $('#console').append(`<p>${date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds()} Error loading training data: ${result.message}</p>`)
                    } else {
                        // Now send data to the server
                        $('#console').append(`<p>${date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds()} Training data validated: ${result.message}</p>`)
                        // Now send the data off to the server. Start loading animation.
                        $('.loader').css('display','block')
                        $.ajax({method: 'POST', url: $SCRIPT_ROOT+'/api/retrain', data: JSON.stringify(data), contentType: 'application/json', success: function() {
                            $('#console').append(`<p>${date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds()} Model successfully retrained</p>`)
                            // Stop loading animation
                            $('.loader').css('display','none')
                        }, error: function() {
                            $('#console').append(`<p>${date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds()} Error retraining model: Internal Error.</p>`)
                            // Stop loading animation
                            $('.loader').css('display','none')
                        }}) 
                    }
                }
            }
            reader.onerror = function() {
                $('#console').append(`<p>${date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds()} Error loading training data: There was an error when reading your file.</p>`)
            }
        }
    })

})

verifyDataset = function(data) {
    for (let i = 0; i < data.length; i++) {
        let row = data[i]
        if (row.length < 2) {
            return {valid: false, message: 'Dataset has incorrect shape'}
        }
        if (row[0] === null || row[1] === null) {
            return {valid: false, message: 'Dataset has missing entries'}
        }
        if ( !(row[1] === 'M' || row[1] === 'F') ) {
            return {valid: false, message: `Dataset labels are incorrect, expecting \'M\' or \'F\' at column 2 of row ${i}`}
        }
    }
    return {valid: true, message: 'Dataset valid, ignoring additional columns.'}
}