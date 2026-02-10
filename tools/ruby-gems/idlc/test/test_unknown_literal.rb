# Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause-Clear

# typed: false
# frozen_string_literal: true

require "idlc"
require "idlc/ast"
require "minitest/autorun"

module Idl
  class TestUnknownLiteral < Minitest::Test
    def test_to_s
      tmp = UnknownLiteral.new(5, 4)
      assert_equal "3'bx01", tmp.to_s

      tmp = UnknownLiteral.new(0x7fff_ffff, 0b1000_0000_0000)
      assert_equal "31'b1111111111111111111x11111111111", tmp.to_s
    end
  end
end
