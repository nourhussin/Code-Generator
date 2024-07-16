`include "adder.v" 
module adder_tb;
//--------------------Parameters---------------------
localparam width = 8;
localparam op_width = 3;
//--------------------Inputs---------------------
reg [width-1 : 0] a_tb;
reg [width-1 : 0] b_tb;
reg [op_width-1 : 0] op_tb;
reg mode_tb;
reg clk_tb;
reg rstn_tb;
//--------------------Outputs---------------------
wire [20-1 : 0] result_tb;
wire flag_tb;
//--------------------Instantiation---------------------
adder #(.width(width),.op_width(op_width)) DUT(
	.a(a_tb),
	.b(b_tb),
	.op(op_tb),
	.mode(mode_tb),
	.clk(clk_tb),
	.rstn(rstn_tb),
	.result(result_tb),
	.flag(flag_tb)
	);
//--------------------Clock Generation---------------------
localparam T = 10;
always#(T/2) clk_tb <= ~clk_tb;
//--------------------Start Testing---------------------
initial begin
	//Reset Inputs:
	clk_tb = 0;
	rstn_tb = 0;

	//Apply Stimulus:

	end
endmodule