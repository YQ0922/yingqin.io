import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.Random;

public class Main extends JFrame implements KeyListener, ActionListener {
    // 遊戲畫面大小
    final int SCREEN_WIDTH = 400;
    final int SCREEN_HEIGHT = 400;

    // 球的初始位置
    final int INIT_Y_POS = SCREEN_HEIGHT / 2;
    final int INIT_X_POS = SCREEN_WIDTH / 2;

    // 擊球板子的大小
    final int PAD_WIDTH = 20;
    final int PAD_HEIGHT = 100;
    final int PLAYER_NUM = 2;
    final int PAD_OFFSET = 10;

    // 更新球位置的計時器
    Timer ballTimer;

    // 球移動的速度
    int ballSpeedX = 1, ballSpeedY = 1;
    final int DELAY_MS = 10;

    // 球的位置
    int ballPosX = INIT_X_POS;
    int ballPosY = INIT_Y_POS;

    // 球的大小
    final int BALL_RADIUS = 20;

    // 球的顏色


    // 隨機數生成器
    Random random = new Random();

    // 玩家移動板子的速度
    int playerSpeedY = 20;

    // 玩家板子的位置
    int[] playerPosX = new int[PLAYER_NUM];
    int[] playerPosY = new int[PLAYER_NUM];

    // 玩家分數
    int[] playerScore = new int[PLAYER_NUM];

    public Main() {
        setTitle("乒乓球");
        setSize(SCREEN_WIDTH, SCREEN_HEIGHT);
        setResizable(false);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        addKeyListener(this);

        initPlayerPos();
        initPlayerScore();
        initBallTimer();
    }

    private void initBallTimer() {
        // 使用 javax.swing.Timer 來定期更新球的位置
        ballTimer = new Timer(DELAY_MS, this);
        ballTimer.start();  // 啟動計時器
    }

    private void initPlayerScore() {
        for (int i = 0; i < PLAYER_NUM; i++) {
            playerScore[i] = 0;
        }
    }

    private void initPlayerPos() {
        for (int i = 0; i < PLAYER_NUM; i++) {
            playerPosY[i] = INIT_Y_POS;
        }

        playerPosX[0] = PAD_WIDTH - PAD_OFFSET;
        playerPosX[1] = SCREEN_WIDTH - PAD_WIDTH - PAD_OFFSET;
    }

    public void update(Graphics g) {
        this.paint(g);
    }

    public void paint(Graphics g) {
        super.paint(g);
        drawPlayerPad(g);
        drawBall(g);
        drawScore(g);
    }

    private void drawPlayerPad(Graphics g) {
        g.setColor(Color.GREEN);
        g.fillRect(playerPosX[0], playerPosY[0], PAD_WIDTH, PAD_HEIGHT);
        g.setColor(Color.BLUE);
        g.fillRect(playerPosX[1], playerPosY[1], PAD_WIDTH, PAD_HEIGHT);
    }

    private void drawBall(Graphics g) {
        // 使用變數 ballColor 來畫球

        g.fillOval(ballPosX, ballPosY, BALL_RADIUS, BALL_RADIUS);
    }

    private void drawScore(Graphics g) {
        g.setColor(Color.BLACK);
        g.drawString("P1:" + playerScore[0], playerPosX[0], 50);
        g.drawString("P2:" + playerScore[1], playerPosX[1] - 50, 50);
    }

    public static void main(String[] args) {
        new Main().setVisible(true);
    }

    @Override
    public void keyPressed(KeyEvent e) {
        int key = e.getKeyCode();

        // Move the player on the left
        if (key == KeyEvent.VK_UP)
            playerPosY[0] -= playerSpeedY;

        if (key == KeyEvent.VK_DOWN)
            playerPosY[0] += playerSpeedY;

        // Move the player on the right
        if (key == KeyEvent.VK_W)
            playerPosY[1] -= playerSpeedY;

        if (key == KeyEvent.VK_X)
            playerPosY[1] += playerSpeedY;

        checkPadPosRange();
        repaint();
    }

    // 檢查板子是否超出遊戲畫面的範圍
    private void checkPadPosRange() {
        for (int i = 0; i < PLAYER_NUM; i++) {
            if (playerPosY[i] < 0) playerPosY[i] = 0;
            if (playerPosY[i] > SCREEN_HEIGHT - PAD_HEIGHT) playerPosY[i] = SCREEN_HEIGHT - PAD_HEIGHT;
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {
    }

    @Override
    public void keyTyped(KeyEvent e) {
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        ballPosX += ballSpeedX;
        ballPosY += ballSpeedY;

        // 球是否碰到遊戲畫面邊界
        if (ballPosX >= SCREEN_WIDTH - BALL_RADIUS || ballPosX <= 0) {
            ballSpeedX = -ballSpeedX;

            if (ballPosX <= 0) {
                playerScore[1]++;
            } else {
                playerScore[0]++;
            }
        }

        if (ballPosY >= SCREEN_HEIGHT - BALL_RADIUS || ballPosY <= BALL_RADIUS) ballSpeedY = -ballSpeedY;

        // 球是否碰到左邊板子
        if (ballPosX <= playerPosX[0] + PAD_WIDTH && ballPosX >= playerPosX[0] &&
                ballPosY <= playerPosY[0] + PAD_HEIGHT && ballPosY >= playerPosY[0]) {
            ballSpeedX = -ballSpeedX;
            // 改變球的顏色

        }

        // 球是否碰到右邊板子
        if (ballPosX <= playerPosX[1] - BALL_RADIUS + PAD_WIDTH && ballPosX >= playerPosX[1] - BALL_RADIUS &&
                ballPosY <= playerPosY[1] + PAD_HEIGHT && ballPosY >= playerPosY[1]) {
            ballSpeedX = -ballSpeedX;
            // 改變球的顏色

        }

        this.repaint();
    }

    // 隨機改變球的顏色

}
