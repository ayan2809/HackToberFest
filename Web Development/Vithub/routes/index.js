exports.index = async function(req, res) {
    var message = '';
    var sess = req.session;
    if (req.method == "POST") {
        var email = req.body.email;
        var username = req.body.username;
        var password = req.body.password;
        if (username && password && email) {
            db.query('SELECT password FROM account WHERE username = ? AND email=?', [username, email], async(error, results) => {
                if (error) throw error;

                if (results.length > 0) {
                    const reslt = await bcrypt.compare(password, results[0].password);
                    console.log(res);
                    if (reslt) {
                        req.session.loggedin = true;
                        req.session.username = username;
                        req.session.email = email;
                        req.session.user = results[0];
                        console.log(username);
                        res.redirect('/dashboard');
                    } else {
                        message = 'Please enter correct password.';
                        res.render('index', { message: message });
                    }
                    res.end();
                } else {
                    message = 'Invalid details';
                    res.render('index', { message: message });
                }
                res.end();
            });
        } else {
            res.send('Please enter Username and Password!');
            res.end();

        }


    } else {
        message = '';
        res.render('index', { message: message });
    }

};

exports.register = async function(req, res) {
    message = '';
    if (req.method == "POST") {
        var emailid = req.body.email;
        var un = req.body.username;
        const pwd = await bcrypt.hash(req.body.password, 10);
        if (un && pwd && emailid) {
            var values = { username: un, password: pwd, email: emailid };
            db.query("INSERT INTO account SET ?", values, function(error, results, fields) {
                if (error) {
                    message = 'Please enter valid details.';
                    res.render('registration', { message: message });
                } else {
                    req.session.loggedin = true;
                    req.session.username = un;
                    req.session.email = emailid;
                    req.session.user = results[0];
                    console.log(un);
                    res.redirect('/dashboard');
                }
            });
        } else {
            message = 'Please enter valid details.';
            res.render('registration', { message: message });
        }


    } else {
        res.render('registration', { message: message });
    }
};





exports.dashboard = function(req, res) {
    username = req.session.username;
    email = req.session.email;
    if (!username && !email) {
        res.redirect("/login");
        return;
    }
    res.render('dashboard', { username: username });
};

exports.logout = function(req, res) {
    req.session.destroy(function(err) {
        res.redirect("/login");
    })
};

exports.profile = function(req, res) {
    username = req.session.username;
    email = req.session.email;
    if (!username && !email) {
        res.redirect("/login");
        return;
    }

    res.render('profile.ejs', { username: username, email: email });
};

exports.cs = function(req, res) {
    username = req.session.username;
    email = req.session.email;
    if (!username && !email) {
        res.redirect("/login");
        return;
    }

    res.render('cs', { username: username, email: email });
};


const { google } = require('googleapis');
const CLIENT_ID = ''
const CLIENT_SECRET = '';
const REDIRECT_URI = '';
const REFRESH_TOKEN = '';
const path = require('path');
const fs = require('fs');
const oauth2Client = new google.auth.OAuth2(
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI
);

oauth2Client.setCredentials({ refresh_token: REFRESH_TOKEN });

const drive = google.drive({
    version: 'v3',
    auth: oauth2Client,
});



exports.uploadFile = async function(req, res) {
    if (req.method == "POST") {
        username = req.session.username;
        var filess = req.file;
        var fname = req.body.filenamess;
        folder_id = '148uViQAoFjoUn1JDobSIh5Y14b_oFVD_';
        if (!filess) {
            message = 'Invalid file';
            username = req.session.username;
            folder_id = '148uViQAoFjoUn1JDobSIh5Y14b_oFVD_';
            email = req.session.email;
            let _RESULT = null;
            try {
                const response = await drive.files.list({
                    pageSize: 150,
                    q: `'148uViQAoFjoUn1JDobSIh5Y14b_oFVD_' in parents`
                });


                if (response && response.data && response.data.files) {
                    _RESULT = response.data.files;
                }
            } catch (ex) { console.log(ex); }
            console.log(_RESULT);
            res.render('upload', { message: message, userData: _RESULT, username: username });
        } else {
            try {
                const response = await drive.files.create({
                    resource: {
                        name: fname, //This can be name of your choice
                        parents: [folder_id],
                    },
                    media: {
                        mimeType: req.file.mimeType,
                        body: fs.createReadStream(filess.path),
                    },
                });
                console.log(response.data);
                message = 'Successful';
                username = req.session.username;
                folder_id = '148uViQAoFjoUn1JDobSIh5Y14b_oFVD_';
                email = req.session.email;
                let _RESULT = null;

                try {

                    const response = await drive.files.list({
                        pageSize: 150,
                        q: `'148uViQAoFjoUn1JDobSIh5Y14b_oFVD_' in parents`
                    });

                    if (response && response.data && response.data.files) {
                        _RESULT = response.data.files;

                    }
                } catch (ex) { console.log(ex); }
                if (!username && !email) {
                    res.redirect("/login");
                    return;
                } else {
                    console.log(_RESULT);
                    res.render('upload', { message: message, userData: _RESULT, username: username });

                }


            } catch (error) {
                console.log(error.message);
            }
        }
    } else {
        username = req.session.username;
        folder_id = '148uViQAoFjoUn1JDobSIh5Y14b_oFVD_';
        email = req.session.email;
        message = '';
        let _RESULT = null;
        try {
            const response = await drive.files.list({
                pageSize: 150,
                q: `'148uViQAoFjoUn1JDobSIh5Y14b_oFVD_' in parents`
            });
            if (response && response.data && response.data.files) {
                _RESULT = response.data.files;
            }
        } catch (ex) { console.log(ex); }
        if (!username && !email) {
            res.redirect("/login");
            return;
        } else {
            console.log(_RESULT);
            res.render('upload', { message: message, userData: _RESULT, username: username });

        }
    }

}


exports.downloadFile = async function(req, res) {
    var text = req.body.butt;
    const myArray = text.split("+");
    var id = myArray[0];
    var name = myArray[1];
    var mimetype = myArray[2].split("/");
    mimetype = mimetype[1];
    var dest = fs.createWriteStream("uploads/" + name + "." + mimetype);
    try {
        file.drive.files.get({ fileId: id, alt: "media" }, { responseType: "stream" },
            (err, { data }) => {
                if (err) {

                    console.log(err);
                    return;
                }
                data
                    .on("end", () => console.log("Done."))
                    .on("error", (err) => {
                        console.log(err);
                        return process.exit();
                    })
                    .pipe(dest);
            }
        );


    } catch (ex) { console.log(ex); }
    var tempFile = "uploads/Aniket-Bansal.pdf";
    fs.readFile(tempFile, function(err, data) {
        res.contentType("application/pdf");
        res.send(data);
    });
};