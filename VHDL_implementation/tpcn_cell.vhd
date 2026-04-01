library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- TPCN cell skeleton:
-- - 10 gated pathways
-- - local delayed error buffer
-- - fixed-point signed arithmetic (Q8.8)
entity tpcn_cell is
  generic (
    PATHWAYS       : positive := 10;
    DATA_WIDTH     : positive := 16;
    ERROR_BUF_SIZE : positive := 8
  );
  port (
    clk            : in  std_logic;
    rst            : in  std_logic;
    en             : in  std_logic;

    -- Current local state/input (Q8.8 signed)
    h_in           : in  signed(DATA_WIDTH - 1 downto 0);

    -- Flattened pathway outputs and gates: pathway k in slice [(k+1)*W-1 : k*W]
    pathway_vals   : in  signed(PATHWAYS * DATA_WIDTH - 1 downto 0);
    pathway_gates  : in  unsigned(PATHWAYS * DATA_WIDTH - 1 downto 0);

    -- Error signal (Q8.8 signed), optionally delayed by buffer
    err_in         : in  signed(DATA_WIDTH - 1 downto 0);
    use_delayed_err: in  std_logic;

    -- Tunables (Q8.8 unsigned)
    leak_alpha     : in  unsigned(DATA_WIDTH - 1 downto 0); -- blending for h memory
    err_gain       : in  unsigned(DATA_WIDTH - 1 downto 0); -- error correction gain

    h_out          : out signed(DATA_WIDTH - 1 downto 0);
    err_out        : out signed(DATA_WIDTH - 1 downto 0)
  );
end entity;

architecture rtl of tpcn_cell is
  subtype sfix_t is signed(DATA_WIDTH - 1 downto 0);
  subtype ufix_t is unsigned(DATA_WIDTH - 1 downto 0);

  type err_buf_t is array (0 to ERROR_BUF_SIZE - 1) of sfix_t;

  signal err_buf      : err_buf_t := (others => (others => '0'));
  signal err_wr_ptr   : integer range 0 to ERROR_BUF_SIZE - 1 := 0;
  signal err_rd_ptr   : integer range 0 to ERROR_BUF_SIZE - 1 := 0;

  signal h_reg        : sfix_t := (others => '0');
  signal mixed_reg    : sfix_t := (others => '0');
  signal selected_err : sfix_t := (others => '0');

  function sat_signed(v : integer; width : positive) return signed is
    variable vmax : integer := 2**(width - 1) - 1;
    variable vmin : integer := -2**(width - 1);
  begin
    if v > vmax then
      return to_signed(vmax, width);
    elsif v < vmin then
      return to_signed(vmin, width);
    else
      return to_signed(v, width);
    end if;
  end function;

begin
  process(clk)
    variable acc_mix      : integer;
    variable p_val_i      : integer;
    variable gate_i       : integer;
    variable mixed_i      : integer;
    variable leak_i       : integer;
    variable err_gain_i   : integer;
    variable h_i          : integer;
    variable err_i        : integer;
    variable next_h_i     : integer;
  begin
    if rising_edge(clk) then
      if rst = '1' then
        h_reg      <= (others => '0');
        mixed_reg  <= (others => '0');
        selected_err <= (others => '0');
        err_buf    <= (others => (others => '0'));
        err_wr_ptr <= 0;
        err_rd_ptr <= 0;
      elsif en = '1' then
        -- Delay line for local error
        err_buf(err_wr_ptr) <= err_in;
        if err_wr_ptr = ERROR_BUF_SIZE - 1 then
          err_wr_ptr <= 0;
        else
          err_wr_ptr <= err_wr_ptr + 1;
        end if;

        if err_rd_ptr = ERROR_BUF_SIZE - 1 then
          err_rd_ptr <= 0;
        else
          err_rd_ptr <= err_rd_ptr + 1;
        end if;

        if use_delayed_err = '1' then
          selected_err <= err_buf(err_rd_ptr);
        else
          selected_err <= err_in;
        end if;

        -- Gated pathway mix: sum_k((pathway_vals_k * pathway_gates_k) / 256)
        acc_mix := 0;
        for k in 0 to PATHWAYS - 1 loop
          p_val_i := to_integer(pathway_vals((k + 1) * DATA_WIDTH - 1 downto k * DATA_WIDTH));
          gate_i  := to_integer(pathway_gates((k + 1) * DATA_WIDTH - 1 downto k * DATA_WIDTH));
          acc_mix := acc_mix + ((p_val_i * gate_i) / 256);
        end loop;

        mixed_reg <= sat_signed(acc_mix, DATA_WIDTH);

        -- h_next = leak_alpha*h_prev + (1-leak_alpha)*mixed - err_gain*err
        h_i        := to_integer(h_reg);
        mixed_i    := to_integer(mixed_reg);
        leak_i     := to_integer(leak_alpha);
        err_gain_i := to_integer(err_gain);
        err_i      := to_integer(selected_err);

        next_h_i := ((leak_i * h_i) / 256)
                    + (((256 - leak_i) * mixed_i) / 256)
                    - ((err_gain_i * err_i) / 256);

        h_reg <= sat_signed(next_h_i, DATA_WIDTH);
      end if;
    end if;
  end process;

  h_out   <= h_reg;
  err_out <= selected_err;
end architecture;
