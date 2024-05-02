-- libraries
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.pkg_edu_bbt.all;

Library UNISIM;
use UNISIM.vcomponents.all;

-- entity
entity hw_top_edu_bbt is
  port(
    clk_i   : in  std_logic;                    --system clock
    arst_i  : in  std_logic;                    --ascynchronous reset
    rx_i    : in  std_logic;                    --receive pin
    tx_o    : out std_logic;
    led_o   : out std_logic_vector(3 downto 0)
  );
end entity hw_top_edu_bbt;

-- architecture
architecture rtl of hw_top_edu_bbt is
 


  component clk_wiz_0
  port
   (-- Clock in ports
    -- Clock out ports
    clk_out1          : out    std_logic;
    -- Status and control signals
    reset             : in     std_logic;
    locked            : out    std_logic;
    clk_in1           : in     std_logic
   );
  end component;
  
    component vio_0
      PORT (
        clk        : in STD_LOGIC;
        probe_out0 : out STD_LOGIC_VECTOR(7 DOWNTO 0);
        probe_out1 : out STD_LOGIC_VECTOR(7 DOWNTO 0);
        probe_out2 : out STD_LOGIC_VECTOR(7 DOWNTO 0);
        probe_out3 : out STD_LOGIC_VECTOR(15 DOWNTO 0);
        probe_out4 : out STD_LOGIC_VECTOR(15 DOWNTO 0);
        probe_out5 : out STD_LOGIC_VECTOR(15 DOWNTO 0);
        probe_out6 : out STD_LOGIC_VECTOR(15 DOWNTO 0)
      );
    end component;
    
    component ila_0
    port (
        clk : IN STD_LOGIC;
        probe0 : IN STD_LOGIC_VECTOR(9 DOWNTO 0); 
        probe1 : IN STD_LOGIC_VECTOR(0 DOWNTO 0); 
        probe2 : IN STD_LOGIC_VECTOR(0 DOWNTO 0); 
        probe3 : IN STD_LOGIC_VECTOR(9 DOWNTO 0); 
        probe4 : IN STD_LOGIC_VECTOR(0 DOWNTO 0); 
        probe5 : IN STD_LOGIC_VECTOR(0 DOWNTO 0); 
        probe6 : IN STD_LOGIC_VECTOR(0 DOWNTO 0);
        probe7 : IN STD_LOGIC_VECTOR(0 DOWNTO 0)
    );
    end component  ;

  signal clk_s        : std_logic;
  signal clk_locked_s : std_logic;

  --signal rx_s : std_logic_vector(0 downto 0);
  signal tx_s : std_logic;

  signal counter_s : std_logic_vector(26 downto 0);

  -- Modulator to channel output
  signal mod_os_data_s  : std_logic_vector( 9 downto 0);
  signal mod_os_dv_s    : std_logic;
  signal mod_os_rfd_s   : std_logic;
  -- Channel output
  signal chan_os_data_s : std_logic_vector( 9 downto 0);
  signal chan_os_dv_s   : std_logic;
  signal chan_os_rfd_s  : std_logic;

  ---- Modem config
  --constant nm1_bytes_c  : std_logic_vector( 7 downto 0) := X"03";
  --constant nm1_pre_c    : std_logic_vector( 7 downto 0) := X"07";
  --constant nm1_sfd_c    : std_logic_vector( 7 downto 0) := X"03";
  --constant det_th_c     : std_logic_vector(15 downto 0) := X"0040";
  --constant pll_kp_c     : std_logic_vector(15 downto 0) := X"A000";
  --constant pll_ki_c     : std_logic_vector(15 downto 0) := X"9000";
  ---- Channel config
  --constant sigma_c      : std_logic_vector(15 downto 0) := X"0040"; -- QU16.12
  
-- Modem config
signal nm1_bytes_s  : std_logic_vector( 7 downto 0);
signal nm1_pre_s    : std_logic_vector( 7 downto 0);
signal nm1_sfd_s    : std_logic_vector( 7 downto 0);
signal det_th_s     : std_logic_vector(15 downto 0);
signal pll_kp_s     : std_logic_vector(15 downto 0);
signal pll_ki_s     : std_logic_vector(15 downto 0);
-- Channel config
signal sigma_s      : std_logic_vector(15 downto 0);

begin

  u_blinky : process(clk_s,arst_i)
  begin
    if arst_i = '1' then
      counter_s <= (others => '0');
    elsif rising_edge(clk_s) then
      counter_s <= std_logic_vector(unsigned(counter_s)+1);
    end if;
  end process;
  led_o <= counter_s(26 downto 23);

--  u_clk_mmcm : clk_wiz_0
--  port map (
--    -- Clock out ports
--    clk_out1 => clk_s,
--    -- Status and control signals
--    reset    => arst_i,
--    locked   => clk_locked_s,
--    -- Clock in ports
--    clk_in1  => clk_i
--  );
--  -- clk_s <= clk_i;

  u_clk_mmcm : clk_wiz_0
     port map ( 
    -- Clock out ports  
     clk_out1 => clk_s,
    -- Status and control signals                
     reset => arst_i,
     locked => open,
     --locked => clk_locked_s,
     -- Clock in ports
     clk_in1 => clk_i
   );

  u_top : top_edu_bbt
  port map
  (
    clk_i  => clk_s,
    arst_i => arst_i,
    rx_i   => rx_i,
    tx_o   => tx_s,
    -- Config
    nm1_bytes_i => nm1_bytes_s,
    nm1_pre_i   => nm1_pre_s,
    nm1_sfd_i   => nm1_sfd_s,
    det_th_i    => det_th_s,
    pll_kp_i    => pll_kp_s,
    pll_ki_i    => pll_ki_s,
    -- Modem to channel
    mod_os_data_o => mod_os_data_s,
    mod_os_dv_o   => mod_os_dv_s,
    mod_os_rfd_i  => mod_os_rfd_s,
    -- Channel to Modem
    chan_os_data_i => chan_os_data_s,
    chan_os_dv_i   => chan_os_dv_s,
    chan_os_rfd_o  => chan_os_rfd_s
  );
  tx_o <= tx_s;

  u_channel : bb_channel
  port map
  (
    -- clk, en, rst
    clk_i         => clk_s,
    en_i          => '1',
    srst_i        => arst_i,
    -- Input Stream
    is_data_i     => mod_os_data_s,
    is_dv_i       => mod_os_dv_s,
    is_rfd_o      => mod_os_rfd_s,
    -- Output Stream
    os_data_o     => chan_os_data_s,
    os_dv_o       => chan_os_dv_s,
    os_rfd_i      => chan_os_rfd_s,
    -- Control
    sigma_i       => sigma_s
  );
  
    u_vio : vio_0
      PORT MAP (
        clk        => clk_i,
        probe_out0 => nm1_bytes_s,
        probe_out1 => nm1_pre_s,
        probe_out2 => nm1_sfd_s,
        probe_out3 => det_th_s,
        probe_out4 => pll_kp_s,
        probe_out5 => pll_ki_s,
        probe_out6 => sigma_s
  );

    u_ila : ila_0
    PORT MAP (
        clk => clk_i,
        probe0    => mod_os_data_s, 
        probe1(0) => mod_os_dv_s, 
        probe2(0) => mod_os_rfd_s, 
        probe3 => chan_os_data_s, 
        probe4(0) => chan_os_dv_s, 
        probe5(0) => chan_os_rfd_s, 
        probe6(0) => (rx_i),
        probe7(0) => (tx_s)
    );

end architecture;

