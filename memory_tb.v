`include "memory.v" 
module memory_tb;
//--------------------Parameters---------------------
localparam width = 32;
localparam depth = 256;
//--------------------Inputs---------------------
reg [depth-1 : 0] address_tb;
reg [20-1 : 0] datain_tb;
reg write_en_tb;
reg clk_tb;
reg rst_tb;
//--------------------Outputs---------------------
wire [width-1 : 0] data_out_tb;
wire full_tb;
//--------------------Instantiation---------------------
memory #(.width(width),.depth(depth)) DUT(
	.address(address_tb),
	.datain(datain_tb),
	.write_en(write_en_tb),
	.clk(clk_tb),
	.rst(rst_tb),
	.data_out(data_out_tb),
	.full(full_tb)
	);
//--------------------Clock Generation---------------------
localparam T = 10;
always#(T/2) clk_tb <= ~clk_tb;
//--------------------Start Testing---------------------
initial begin
	//Reset Inputs:
	clk_tb = 0;
	rst_tb = 1;

	//Apply Stimulus:

	end
endmodule