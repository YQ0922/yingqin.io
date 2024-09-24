//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

import java.awt.Color;
import java.awt.Component;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import javax.swing.JFrame;
import javax.swing.Timer;

public class Main extends JFrame implements KeyListener, ActionListener {
    final int SCREEN_WIDTH = 400;
    final int SCREEN_HEIGHT = 400;
    final int INIT_Y_POS = 200;
    final int INIT_X_POS = 200;
    final int PAD_WIDTH = 20;
    final int PAD_HEIGHT = 100;
    final int PLAYER_NUM = 2;
    final int PAD_OFFSET = 10;
    Timer ballTimer;
    int ballSpeedX = 1;
    int ballSpeedY = 1;
    final int DELAY_MS = 10;
    int ballPosX = 200;
    int ballPosY = 200;
    final int BALL_RADIUS = 20;
    int playerSpeedY = 20;
    int[] playerPosX = new int[2];
    int[] playerPosY = new int[2];
    int[] playerScore = new int[2];

    public Main() {
        this.setTitle("乒乓球");
        this.setSize(400, 400);
        this.setResizable(false);
        this.setDefaultCloseOperation(3);
        this.setLocationRelativeTo((Component)null);
        this.addKeyListener(this);
        this.initPlayerPos();
        this.initPlayerScore();
        this.initBallTimer();
    }

    private void initBallTimer() {
        this.ballTimer = new Timer(10, this);
        this.ballTimer.start();
    }

    private void initPlayerScore() {
        for(int i = 0; i < 2; ++i) {
            this.playerScore[i] = 0;
        }

    }

    private void initPlayerPos() {
        for(int i = 0; i < 2; ++i) {
            this.playerPosY[i] = 200;
        }

        this.playerPosX[0] = 10;
        this.playerPosX[1] = 370;
    }

    public void update(Graphics g) {
        this.paint(g);
    }

    public void paint(Graphics g) {
        super.paint(g);
        this.drawPlayerPad(g);
        this.drawBall(g);
        this.drawScore(g);
    }

    private void drawPlayerPad(Graphics g) {
        g.setColor(Color.GREEN);
        g.fillRect(this.playerPosX[0], this.playerPosY[0], 20, 100);
        g.setColor(Color.BLUE);
        g.fillRect(this.playerPosX[1], this.playerPosY[1], 20, 100);
    }

    private void drawBall(Graphics g) {
        g.setColor(Color.CYAN);
        g.fillOval(this.ballPosX, this.ballPosY, 20, 20);
    }

    private void drawScore(Graphics g) {
        g.setColor(Color.BLACK);
        g.drawString("P1:" + this.playerScore[0], this.playerPosX[0], 50);
        g.drawString("P2:" + this.playerScore[1], this.playerPosX[1] - 50, 50);
    }

    public static void main(String[] args) {
        (new Main()).setVisible(true);
    }

    public void keyPressed(KeyEvent e) {
        int key = e.getKeyCode();
        int[] var10000;
        if (key == 38) {
            var10000 = this.playerPosY;
            var10000[0] -= this.playerSpeedY;
        }

        if (key == 40) {
            var10000 = this.playerPosY;
            var10000[0] += this.playerSpeedY;
        }

        if (key == 87) {
            var10000 = this.playerPosY;
            var10000[1] -= this.playerSpeedY;
        }

        if (key == 88) {
            var10000 = this.playerPosY;
            var10000[1] += this.playerSpeedY;
        }

        this.checkPadPosRange();
        this.repaint();
    }

    private void checkPadPosRange() {
        for(int i = 0; i < 2; ++i) {
            if (this.playerPosY[i] < 0) {
                this.playerPosY[i] = 0;
            }

            if (this.playerPosY[i] > 300) {
                this.playerPosY[i] = 300;
            }
        }

    }

    public void keyReleased(KeyEvent e) {
    }

    public void keyTyped(KeyEvent e) {
    }

    public void actionPerformed(ActionEvent e) {
        this.ballPosX += this.ballSpeedX;
        this.ballPosY += this.ballSpeedY;
        if (this.ballPosX >= 380 || this.ballPosX <= 0) {
            this.ballSpeedX = -this.ballSpeedX;
            int var10002;
            if (this.ballPosX <= 0) {
                var10002 = this.playerScore[1]++;
            } else {
                var10002 = this.playerScore[0]++;
            }
        }

        if (this.ballPosY >= 380 || this.ballPosY <= 20) {
            this.ballSpeedY = -this.ballSpeedY;
        }

        if (this.ballPosX <= this.playerPosX[0] + 20 && this.ballPosX >= this.playerPosX[0] && this.ballPosY <= this.playerPosY[0] + 100 && this.ballPosY >= this.playerPosY[0]) {
            this.ballSpeedX = -this.ballSpeedX;
        }

        if (this.ballPosX <= this.playerPosX[1] - 20 + 20 && this.ballPosX >= this.playerPosX[1] - 20 && this.ballPosY <= this.playerPosY[1] + 100 && this.ballPosY >= this.playerPosY[1]) {
            this.ballSpeedX = -this.ballSpeedX;
        }

        this.repaint();
    }
}
