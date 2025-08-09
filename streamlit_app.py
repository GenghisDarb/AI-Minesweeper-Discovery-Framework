 
    st.title("AI Minesweeper Discovery Framework")
import json
import tempfile
import streamlit as st
from ai_minesweeper.meta_cell_confidence.confidence import BetaConfidence
from ai_minesweeper.board_builder import BoardBuilder
from ai_minesweeper.risk_assessor import RiskAssessor
from ai_minesweeper.ui_widgets import (
    apply_grid_styling,
    color_coded_cell_rendering,
    render_unresolved_hypotheses,
    render_revealed_hypotheses_summary,
    highlight_newly_revealed_cells,
    display_confidence,
)
 
from ai_minesweeper.torus_recursion.dpp14_recursion_engine import DPP14RecursionEngine


    st.title("AI Minesweeper Discovery Framework")

    # Initialize session state variables
    if "board" not in st.session_state:
        st.session_state.board = None
    if "solver" not in st.session_state:
        st.session_state.solver = None
    if "beta_confidence" not in st.session_state:
        st.session_state.beta_confidence = BetaConfidence()
    if "revealed_hypotheses" not in st.session_state:
        st.session_state.revealed_hypotheses = []
    if "solver_paused" not in st.session_state:
        st.session_state.solver_paused = True
    if "confidence_history" not in st.session_state:
        st.session_state.confidence_history = []

    # Define toggles for execution modes
    step_by_step = st.sidebar.checkbox("Step-by-step mode", value=True)
    auto_discover = st.sidebar.checkbox("Auto-discover (run continuously)", value=False)

    # Upload CSV board
    csv_file = st.file_uploader("Upload a CSV board", type=["csv"])

    if csv_file:
        board = BoardBuilder.from_csv(csv_file)
        
    def setup_logging(self):
        """Configure logging for the application."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if 'board' not in st.session_state:
            st.session_state.board = None
        if 'solver' not in st.session_state:
            st.session_state.solver = None
        if 'visualizer' not in st.session_state:
            st.session_state.visualizer = None
        if 'game_started' not in st.session_state:
            st.session_state.game_started = False
        if 'auto_solve_running' not in st.session_state:
            st.session_state.auto_solve_running = False
        if 'move_history' not in st.session_state:
            st.session_state.move_history = []
        if 'last_action' not in st.session_state:
            st.session_state.last_action = None
    
    def run(self):
        """Run the main Streamlit application."""
        st.title("🧠 AI Minesweeper - χ-Recursive Form v1.1.0")
        st.markdown("*Advanced AI with TORUS theory integration and meta-cell confidence*")
        
        # Sidebar controls
        self.create_sidebar()
        
        # Main content area
        
        with col1:
            self.create_game_board()
        
        with col2:
            self.create_control_panel()
            self.create_statistics_panel()
        
        # Bottom panels
        self.create_visualization_panels()
    
    def create_sidebar(self):
        """Create the sidebar with game configuration."""
        st.sidebar.header("🎮 Game Configuration")
        
        # Game parameters
        width = st.sidebar.slider("Board Width", 5, 20, 9)
        height = st.sidebar.slider("Board Height", 5, 20, 9)
        mine_density = st.sidebar.slider("Mine Density (%)", 10, 30, 15)
        mines = int((width * height * mine_density) / 100)
        
        st.sidebar.write(f"**Mines:** {mines}")
        
        # AI Configuration
        st.sidebar.header("🤖 AI Configuration")
        meta_mode = st.sidebar.checkbox("Meta-cell confidence mode", value=True)
        high_contrast = st.sidebar.checkbox("High contrast mode", value=False)
        show_risk_overlay = st.sidebar.checkbox("Show risk overlay", value=True)
        
        # Game controls
        st.sidebar.header("🎯 Game Controls")
        
        if st.sidebar.button("🚀 New Game", type="primary"):
            self.start_new_game(width, height, mines, meta_mode, high_contrast)
        
        if st.session_state.game_started:
            if st.sidebar.button("🧠 AI Move"):
                self.make_ai_move()
            
            auto_solve = st.sidebar.button("⚡ Auto-Solve")
            if auto_solve and not st.session_state.auto_solve_running:
                st.session_state.auto_solve_running = True
                st.rerun()
            
            if st.session_state.auto_solve_running:
                if st.sidebar.button("⏹️ Stop Auto-Solve"):
                    st.session_state.auto_solve_running = False
                else:
                    self.auto_solve_step()
        
        # Store configuration in session state
        st.session_state.show_risk_overlay = show_risk_overlay
        st.session_state.meta_mode = meta_mode
    
    def start_new_game(self, width: int, height: int, mines: int, meta_mode: bool, high_contrast: bool):
        """Start a new game with specified parameters."""
        st.session_state.board = Board(width, height, mines)
        st.session_state.solver = ConstraintSolver()
        st.session_state.visualizer = MinesweeperVisualizer(high_contrast=high_contrast)
        st.session_state.tooltip_manager = TooltipManager()
        st.session_state.game_started = False
        st.session_state.auto_solve_running = False
        st.session_state.move_history = []
        st.session_state.last_action = None
        st.session_state.meta_mode = meta_mode
        
        st.success(f"New {width}x{height} game created with {mines} mines!")
        self.logger.info(f"New game started: {width}x{height}, {mines} mines, meta_mode={meta_mode}")
    
    def create_game_board(self):
        """Create the interactive game board visualization."""
        st.header("🎯 Game Board")
        
        if st.session_state.board is None:
            st.info("👆 Configure and start a new game in the sidebar!")
            return
        
        board = st.session_state.board
        
        # Game status
        status_col1, status_col2, status_col3 = st.columns(3)
        
        with status_col1:
            st.metric("Remaining Mines", board.remaining_mines)
        
        with status_col2:
            moves = len(st.session_state.move_history)
            st.metric("Moves Made", moves)
        
        with status_col3:
            if board.is_solved():
                st.success("🎉 SOLVED!")
            elif st.session_state.game_started:
                st.info("🎮 Playing...")
            else:
                st.warning("🔸 Click to start")
        
        # Board visualization
        try:
            # Get risk map if available
            risk_map = None
            if (st.session_state.get('show_risk_overlay', False) and 
                st.session_state.solver and st.session_state.game_started):
                risk_map = st.session_state.solver.risk_assessor.calculate_risk_map(board)
            
            # Create visualization
            fig = st.session_state.visualizer.create_board_visualization(
                board, 
                risk_map=risk_map,
                confidence_overlay=st.session_state.get('show_risk_overlay', False)
            )
            
            st.pyplot(fig)
            plt.close(fig)  # Free memory
            
        except Exception as e:
            st.error(f"Error creating board visualization: {e}")
            self.logger.error(f"Visualization error: {e}")
        
        # Interactive controls
        if st.session_state.board and not board.is_solved():
            self.create_interactive_controls()
    
    def create_interactive_controls(self):
        """Create interactive controls for manual moves."""
        st.subheader("🎮 Manual Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            x = st.number_input("X Coordinate", 0, st.session_state.board.width-1, 0)
            y = st.number_input("Y Coordinate", 0, st.session_state.board.height-1, 0)
        
        with col2:
            if st.button("🔍 Reveal Cell"):
                self.manual_reveal(x, y)
            
            if st.button("🚩 Flag Cell"):
                self.manual_flag(x, y)
    
    def manual_reveal(self, x: int, y: int):
        """Handle manual cell reveal."""
        board = st.session_state.board
        
        if not st.session_state.game_started:
            # First move - place mines and start game
            board.place_mines((x, y))
            st.session_state.game_started = True
        
        success = board.reveal_cell(x, y)
        self.record_move("reveal", (x, y), success)
        
        if not success:
            st.error(f"💥 Mine hit at ({x}, {y})! Game Over.")
        elif board.is_solved():
            st.success("🎉 Congratulations! Board solved!")
        
        st.rerun()
    
    def manual_flag(self, x: int, y: int):
        """Handle manual cell flagging."""
        board = st.session_state.board
        
        if board.cell_states[(x, y)] == CellState.HIDDEN:
            board.flag_cell(x, y)
            self.record_move("flag", (x, y), True)
            st.rerun()
        elif board.cell_states[(x, y)] in [CellState.FLAGGED, CellState.SAFE_FLAGGED]:
            board.unflag_cell(x, y)
            self.record_move("unflag", (x, y), True)
            st.rerun()
    
    def make_ai_move(self):
        """Make one AI move."""
        if not st.session_state.game_started:
            # Auto-start the game
            center_x = st.session_state.board.width // 2
            center_y = st.session_state.board.height // 2
            st.session_state.board.place_mines((center_x, center_y))
            st.session_state.board.reveal_cell(center_x, center_y)
            st.session_state.game_started = True
            self.record_move("reveal", (center_x, center_y), True)
        
        solution = st.session_state.solver.solve_step(st.session_state.board)
        
        if solution["action"] == "none":
            st.warning("AI: No valid moves found.")
            return
        elif solution["action"] == "contradiction":
            st.error("AI: Contradiction detected in board state!")
            return
        
        action = solution["action"]
        position = solution["position"]
        confidence = solution.get("confidence", 0.5)
        reason = solution.get("reason", "No reason provided")
        
        # Execute the move
        success = True
        if action == "reveal":
            success = st.session_state.board.reveal_cell(*position)
        elif action == "flag":
            safe_flag = st.session_state.meta_mode and confidence < 0.9
            st.session_state.board.flag_cell(*position, safe_flag=safe_flag)
        
        # Update solver and record move
        st.session_state.solver.update_outcome(action, position, success, st.session_state.board)
        self.record_move(action, position, success, ai_move=True, confidence=confidence, reason=reason)
        
        # Update UI
        if not success:
            st.error(f"💥 AI hit a mine at {position}! Game Over.")
            st.session_state.auto_solve_running = False
        elif st.session_state.board.is_solved():
            st.success("🎉 AI solved the board!")
            st.session_state.auto_solve_running = False
        
        st.rerun()
    
    def auto_solve_step(self):
        """Perform one step of auto-solving."""
        if not st.session_state.board.is_solved():
            self.make_ai_move()
            time.sleep(0.5)  # Brief pause for visualization
        else:
            st.session_state.auto_solve_running = False
    
    def record_move(self, action: str, position: Tuple[int, int], success: bool, 
                   ai_move: bool = False, confidence: float = None, reason: str = None):
        """Record a move in the history."""
        move_record = {
            "move_number": len(st.session_state.move_history) + 1,
            "action": action,
            "position": position,
            "success": success,
            "ai_move": ai_move,
            "confidence": confidence,
            "reason": reason,
            "timestamp": time.time()
        }
        
        st.session_state.move_history.append(move_record)
        st.session_state.last_action = move_record
    
    def create_control_panel(self):
        """Create the AI control and information panel."""
        st.header("🤖 AI Control Panel")
        
        if not st.session_state.solver:
            st.info("Start a game to see AI controls")
            return
        
        # Current AI status
        if st.session_state.last_action and st.session_state.last_action["ai_move"]:
            last = st.session_state.last_action
            st.write(f"**Last AI Action:** {last['action']} at {last['position']}")
            if last['confidence']:
                st.write(f"**Confidence:** {last['confidence']:.3f}")
            if last['reason']:
                st.write(f"**Reason:** {last['reason']}")
        
        # AI recommendation
        if st.session_state.game_started and not st.session_state.board.is_solved():
            try:
                recommendation = st.session_state.solver.solve_step(st.session_state.board)
                
                if recommendation["action"] != "none":
                    st.subheader("💡 AI Recommendation")
                    st.write(f"**Action:** {recommendation['action']} at {recommendation.get('position', 'N/A')}")
                    st.write(f"**Confidence:** {recommendation.get('confidence', 0.5):.3f}")
                    st.write(f"**Reason:** {recommendation.get('reason', 'No reason')}")
            except Exception as e:
                st.error(f"Error getting AI recommendation: {e}")
    
    def create_statistics_panel(self):
        """Create the statistics and performance panel."""
        st.header("📊 Statistics")
        
        if not st.session_state.solver:
            return
        
        try:
            stats = st.session_state.solver.get_solver_statistics()
            
            # Basic stats
            st.subheader("🎯 Game Statistics")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Solver Iterations", stats.get('solver_iterations', 0))
                st.metric("Active Constraints", stats.get('active_constraints', 0))
            
            with col2:
                st.metric("χ-Cycle Progress", stats.get('chi_cycle_progress', 0))
                current_confidence = stats.get('policy_stats', {}).get('confidence_stats', {}).get('current_confidence', 0)
                st.metric("Current Confidence", f"{current_confidence:.3f}")
            
            # Performance metrics
            if st.session_state.move_history:
                ai_moves = [m for m in st.session_state.move_history if m['ai_move']]
                if ai_moves:
                    success_rate = len([m for m in ai_moves if m['success']]) / len(ai_moves)
                    avg_confidence = sum([m['confidence'] for m in ai_moves if m['confidence']]) / len([m for m in ai_moves if m['confidence']])
                    
                    st.subheader("🎯 AI Performance")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Success Rate", f"{success_rate:.1%}")
                    with col2:
                        st.metric("Avg Confidence", f"{avg_confidence:.3f}")
        
        except Exception as e:
            st.error(f"Error displaying statistics: {e}")
    
    def create_visualization_panels(self):
        """Create additional visualization panels."""
        if not st.session_state.solver or not st.session_state.board:
            return
        
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["📈 Confidence Trends", "🎯 Risk Analysis", "📜 Move History"])
        
        with tab1:
            self.create_confidence_visualization()
        
        with tab2:
            self.create_risk_analysis()
        
        with tab3:
            self.create_move_history()

 
    
    def create_confidence_visualization(self):
        """Create confidence trend visualization."""
        st.subheader("📈 χ-Recursive Confidence Evolution")
        
        try:
            confidence_history = st.session_state.board.confidence_history
            chi_cycle_count = st.session_state.board.chi_cycle_count
            
            if confidence_history:
                fig = st.session_state.visualizer.create_chi_cycle_visualization(
                    confidence_history, chi_cycle_count
                )
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.info("No confidence data available yet. Make some AI moves to see trends.")
        
        except Exception as e:
            st.error(f"Error creating confidence visualization: {e}")
    
    def create_risk_analysis(self):
        """Create risk analysis visualization."""
        st.subheader("🎯 Risk Assessment Analysis")
        
        try:
            if st.session_state.game_started:
                risk_map = st.session_state.solver.risk_assessor.calculate_risk_map(st.session_state.board)
                
                if risk_map:
                    fig = st.session_state.visualizer.create_risk_distribution_plot(risk_map)
                    st.pyplot(fig)
                    plt.close(fig)
                    
                    # Risk statistics table
                    risk_stats = st.session_state.solver.risk_assessor.get_risk_statistics(st.session_state.board)
                    if "error" not in risk_stats:
                        st.subheader("📊 Risk Statistics")
                        stats_df = pd.DataFrame([risk_stats])
                        st.dataframe(stats_df)
                else:
                    st.info("No hidden cells to analyze.")
            else:
                st.info("Start the game to see risk analysis.")
        
        except Exception as e:
            st.error(f"Error creating risk analysis: {e}")
    
    def create_move_history(self):
        """Create move history table."""
        st.subheader("📜 Move History")
        
        if st.session_state.move_history:
            # Create DataFrame from move history
            df_data = []
            for move in st.session_state.move_history:
                df_data.append({
                    "Move": move["move_number"],
                    "Action": move["action"],
                    "Position": f"({move['position'][0]}, {move['position'][1]})",
                    "Success": "✅" if move["success"] else "❌",
                    "Player": "🤖 AI" if move["ai_move"] else "👤 Human",
                    "Confidence": f"{move['confidence']:.3f}" if move["confidence"] else "N/A"
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # Download button for move history
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download Move History",
                csv,
                "minesweeper_moves.csv",
                "text/csv"
            )
        else:
            st.info("No moves recorded yet.")


def main():
    """Main entry point for the Streamlit application."""
    app = StreamlitMinesweeperApp()
    app.run()


if __name__ == "__main__":
    main()
 
