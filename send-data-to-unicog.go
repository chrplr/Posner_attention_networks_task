// send data to a remote server using sftp
// Time-stamp: <2023-04-09 10:27:27 christophe@pallier.org>

package main

import (
	"strings"
	"fmt"
	"log"
	"errors"
	"time"
	"os"
	"os/user"
	"syscall"
	"encoding/base64"
	"path/filepath"
	"github.com/pkg/sftp"
	"golang.org/x/crypto/ssh"
	"golang.org/x/crypto/bcrypt"
	"golang.org/x/term"
)



type serverParams struct  {
	server string
	login string
	passwd string
	folder string 
}


// The server password is xor-ed with the password to enter on the command line // The other fields are in base64 to avoid easy spotting by a google search 
var private_unicog = serverParams{"bnM1MzMzNDMuaXAtMTk4LTI0NS02MS5uZXQ6MjI=",
	"Z3Vlc3RfbGFi", string([]byte{2, 24, 65, 65, 78, 74, 10, 60}), "cGFydGFnZS9wcmVtcw=="}

const pwHash string = "$2a$14$VNn0K9SPc9zuisFr.B2DeuY6PihRpIdao2jh.9IwdtKvqsQZlB2DG"

const contactEmail = "christophe@pallier.org"


func (p *serverParams) decodeParams(passwd string) error {
	var buf []byte
	var err error
	
	if buf, err = base64.StdEncoding.DecodeString(p.server); err != nil {
		return err
	}
	p.server = string(buf)
	
	if buf, err = base64.StdEncoding.DecodeString(p.login); err != nil {
		return err
	}
	p.login = string(buf)

	p.passwd = XorStrings(p.passwd, passwd)

	if buf, err = base64.StdEncoding.DecodeString(p.folder); err != nil {
		return err
	}
	p.folder = string(buf)
	
	return nil
}



// copy a localfile to remote sftp server
func SendFileToSftpServer(localFile string, dstPath string,  param serverParams) error {
	config := &ssh.ClientConfig{
		User: param.login,
		Auth: []ssh.AuthMethod{
			ssh.Password(param.passwd),
		},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
	}

	connection, err := ssh.Dial("tcp", param.server, config)
	if err != nil {
		return fmt.Errorf("ssh.Dial %s", err)
	}
	defer connection.Close()

	sftp, err := sftp.NewClient(connection)
	if err != nil {
		return fmt.Errorf("sftp.NewClient %s",err)
	}
	defer sftp.Close()

	srcFile, err := os.Open(localFile)
	if err != nil {
		return fmt.Errorf("os.Open %s: %s", localFile, err)
	}
	defer srcFile.Close()

	dstFile, err := sftp.Create(dstPath)
	if err != nil {
		return fmt.Errorf("sftp.Create %s: %s ", dstPath, err)
	}
	defer dstFile.Close()

	// write to destination
	if _, err := dstFile.ReadFrom(srcFile); err != nil {
		return fmt.Errorf("Error during file transfert: %s", err)
	}
	return nil
}


// ReadPassword reads a password on the Terminal without echoing
func ReadPassword() (string, error) {
    fmt.Print("Enter Password: ")
    bytePassword, err := term.ReadPassword(int(syscall.Stdin))
    if err != nil {
        return "", err
    }

    password := string(bytePassword)
    return strings.TrimSpace(password), nil
}


func CheckPasswordHash(password, hash string) bool {
    err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
    return err == nil
}

func XorStrings(main, key string) string {
	bmain := []byte(main)
	lmain := len(bmain)

	bkey := []byte(key)
	lkey := len(bkey)
	// extend the size of bkey to match that of bmain if necessary
	for i := lkey; i < lmain; i++ {
	        bkey =append(bkey, bkey[i % lkey])
	}
	c := make([]byte, lmain)
	for i := 0; i < lmain; i++ {
		c[i] = bmain[i] ^ bkey[i]
	}
	return string(c)
}


func GetCurrentTimeStamp() string {
	currentTime := time.Now()
	return currentTime.Format(time.RFC3339)
}

func GetHostName() string {
	hostname, err := os.Hostname()
        if err != nil {
            log.Fatalf("couldn't determine hostname: %v", err)
        }
	return hostname
}

func GetUserName() string {
	currentUser, err := user.Current()
	if err != nil {
		log.Fatalf(err.Error())
	}
	return  currentUser.Username
}


func addInfoToFileName(fname, info string) string {
	ext := filepath.Ext(fname)
	basename := strings.TrimSuffix(fname, ext)
	return basename + info + ext
}

func main() {
	if len(os.Args) != 2 {
		log.Fatal("Expected a single filename as argument")
	}

	fileToSend := os.Args[1]

	if _, err := os.Stat(fileToSend); errors.Is(err, os.ErrNotExist) {
		log.Fatalf("Unknown file: %s", fileToSend)
	}

	passwd, err  := ReadPassword()
	if err != nil {
		log.Fatal(err)
	}


        if !CheckPasswordHash(passwd, pwHash) {
		time.Sleep(1 * time.Second)
		log.Fatalf("\nPassword incorrect. Contact <%s>", contactEmail)
	}

	private_unicog.decodeParams(passwd)

	dstFile := sftp.Join(private_unicog.folder, addInfoToFileName(fileToSend, "_" + "host-" + GetHostName() + "_" + "user-" + GetUserName() + "_" + "date-" + GetCurrentTimeStamp()))
	fmt.Printf("\nTransfering '%s' to '%s' as '%s'\n", fileToSend, private_unicog.server, dstFile)

	if err := SendFileToSftpServer(fileToSend, dstFile, private_unicog); err != nil {
		log.Fatalf("%s", err)
	}
	fmt.Println("Done.")
}
