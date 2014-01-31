package main

import "wishbone/router"
import "wishbone/module/output/stdout"
import "wishbone/module/input/testevent"
import "wishbone/module/flow/roundrobin"

func main() {

	router := router.NewRouter()
	input := testevent.NewModule("input", "Hello")
	roundrobin := roundrobin.NewModule("roundrobin")
	output1 := stdout.NewModule("output1", false)
	output2 := stdout.NewModule("output2", false)

	router.Register(&input)
	router.Register(&roundrobin)
	router.Register(&output1)
	router.Register(&output2)

	router.Connect("input.outbox", "roundrobin.inbox")
	router.Connect("roundrobin.outbox1", "output1.inbox")
	router.Connect("roundrobin.outbox2", "output2.inbox")

	router.Start()
	router.Block()
}
