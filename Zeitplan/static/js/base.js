function main() {
    // Clear cookies
    $('#clearCookiesButton').on("click", function(){
        console.log("Clearing cookies...");
        var allCookies = document.cookie.split(';'); 
                
        // The "expire" attribute of every cookie is
        // Set to "Thu, 01 Jan 1970 00:00:00 GMT"
        for (var i = 0; i < allCookies.length; i++) 
            document.cookie = allCookies[i] + "=;expires=" + new Date(0).toUTCString(); 
        console.log("Cookies cleared!");
        $('#clearCookiesModal').modal('show');
        setTimeout(() => {
            document.location.href = '/Zeitplan';
        }, 5000);
    });
}

main();

/*
References:
    https://www.geeksforgeeks.org/how-to-clear-all-cookies-using-javascript/
*/