/*
 * This file was automatically generated by EvoSuite
 * Tue Sep 04 16:17:00 GMT 2018
 */

package br.ufal.ic.masg.operations;

import org.junit.Test;
import static org.junit.Assert.*;
import br.ufal.ic.masg.operations.GreaterOrEqualThan;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class GreaterOrEqualThan_ESTest extends GreaterOrEqualThan_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test0()  throws Throwable  {
      GreaterOrEqualThan greaterOrEqualThan0 = new GreaterOrEqualThan();
      boolean boolean0 = greaterOrEqualThan0.function(0, (-1887));
      assertTrue(boolean0);
  }

  @Test(timeout = 4000)
  public void test1()  throws Throwable  {
      GreaterOrEqualThan greaterOrEqualThan0 = new GreaterOrEqualThan();
      boolean boolean0 = greaterOrEqualThan0.function((-625), (-625));
      assertTrue(boolean0);
  }

  @Test(timeout = 4000)
  public void test2()  throws Throwable  {
      GreaterOrEqualThan greaterOrEqualThan0 = new GreaterOrEqualThan();
      boolean boolean0 = greaterOrEqualThan0.function((-781), (-625));
      assertFalse(boolean0);
  }
}