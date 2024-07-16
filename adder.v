module adder #(parameter width = 8, op_width = 3)( 
//--------------------Input Ports---------------------
input wire [width-1 : 0] a,
input wire [width-1 : 0] b,
input wire [op_width-1 : 0] op,
input wire mode,
input wire clk,
input wire rstn,
//--------------------Output Ports---------------------
output reg [20-1 : 0] result,
output wire flag
);
//--------------------Internal Variables---------------------

//--------------------Design Implementation---------------------
always @(posedge clk)
begin
	if (rstn == 0)
	begin
	//--------------------Reset Conditions---------------------

	end

	else
	begin
	//--------------------Your Design---------------------

	end
end

endmodule