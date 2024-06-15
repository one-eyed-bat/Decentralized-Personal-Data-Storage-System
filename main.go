packge main

import (
	"fmt"
	"os"

	shell "github.com/ipfs/go-ipfs-api"
)

func DownloadFile(cid *C.char) *C.char {
	sh := shell.NewShell("localhost:5001")
	hash := C.GoString(cid)

	data , err := sh.Cat(has)
	if err != nil {
		return C.Cstring("")
	}
	return C.Cstring(string(data))


func main() {}
