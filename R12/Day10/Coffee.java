

/* Decompiler 7ms, total 292ms, lines 73 */
import java.math.BigInteger;
import java.util.Scanner;

public class Main {
   public static void main(String[] var0) {
      if (phase1() && phase2()) {
         BigInteger var1 = BigInteger.valueOf((long)phase3());
         if (var1 != BigInteger.valueOf(0L)) {
            var1 = var1.multiply(new BigInteger("1774644555281433326593995747891879112794844969863978577734152855605111785335667760583361496676349225814051648061346266137738845404784964123587298"));
            var1 = var1.add(new BigInteger("2005646691"));
            BigInteger var2 = var1;
            var1 = var1.add(new BigInteger("3152844105823862817153505108800338993847935220109223044243415703869202589182287984111789276617299563428157322540964972770115423280689072635053796538006552"));
            BigInteger var3 = var1;
            var1 = var1.add(new BigInteger("4520540198980111894921105365501264712623944875342972337398443790071092322580676583371926617157121459607700639361089023120555663451319258149276786423891658"));
            BigInteger var5 = var3.modPow(var2, var1);
            String var6 = new String(var5.toByteArray());
            System.out.println("Great work!");
            System.out.print("Here's your flag: ");
            System.out.print(var6);
         }
      }

   }

   public static boolean phase1() {
      System.out.println("ENTERING ===PHASE 1===");
      System.out.print("Enter the password: ");
      Scanner var0 = new Scanner(System.in);
      String var1 = var0.nextLine();
      int[] var2 = new int[]{104, 111, 116, 99, 117, 112, 111, 102, 99, 111, 102, 102, 101, 101};

      for(int var3 = 0; var3 < var1.length(); ++var3) {
         char var4 = var1.charAt(var3);
         if (var4 != var2[var3]) {
            return false;
         }
      }

      return var2.length == var1.length();
   }

   public static boolean phase2() {
      System.out.println("ENTERING ===PHASE 2===");
      Scanner var0 = new Scanner(System.in);
      int var1 = 1;

      for(int var2 = 1; var2 < 6; ++var2) {
         int var3 = var1;
         System.out.printf("var3 = %d, var2 = %d%n", var3, var2);
         var1 = var0.nextInt();
         if (var1 / var3 != var2) {
            System.out.println("Nope!");
            return false;
         }
         
      }

      return true;
   }

   public static int phase3() {
      System.out.println("ENTERING ===PHASE 3===");
      Scanner var0 = new Scanner(System.in);
      byte var1 = -1;
      int var3 = var0.nextInt();
      if (var3 == var1) {
         return 0;
      } else {
         int var2 = var3;
         var3 *= 2;
         ++var3;
         return var1 == var3 ? var2 : 0;
      }
   }
}
