// Adicione o código JavaScript aqui

// Quando a página for carregada, coloque o cursor na caixa de entrada
window.onload = function() {
    document.getElementById("input").focus();
  }
  
  // Quando o usuário pressionar o botão de envio, envie a mensagem para o chatbot
  document.getElementById("submit").onclick = function() {
    var input = document.getElementById("input").value;
    document.getElementById("output").innerHTML += "Você: " + input + "<br>";
  
    // Envie a mensagem para o servidor Python usando XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/chatbot");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
      if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        var response = JSON.parse(this.responseText)["response"];
        document.getElementById("output").innerHTML += "ChatBot: " + response + "<br>";
        document.getElementById("input").value = "";
      }
    };
    xhr.send(JSON.stringify({"message": input}));
  }