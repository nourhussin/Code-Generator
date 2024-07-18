module memory #(parameter width = 32, depth = 256)( 
//--------------------Input Ports---------------------
input wire [depth-1 : 0] address,
input wire [20-1 : 0] datain,
input wire write_en,
input wire clk,
input wire rst,
//--------------------Output Ports---------------------
output wire [width-1 : 0] data_out,
output wire full
);
//--------------------Internal Variables---------------------

//--------------------Design Implementation---------------------
always @(posedge clk, posedge rst)
begin
	if (rst == 1)
	begin
	//--------------------Reset Conditions---------------------

	end

	else
	begin
	//--------------------Your Design---------------------

	end
end

endmodule